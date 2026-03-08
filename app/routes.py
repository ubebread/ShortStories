# story_writer/app/routes.py
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from .models import db, Story
from .story_engine import generate_story
import uuid

main = Blueprint('main', __name__)

MAX_IDEAS_LEN = 1000

@main.route('/', methods=['GET', 'POST'])
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    if request.method == 'POST':
        age_raw = request.form.get('age', '').strip()
        ideas = request.form.get('ideas', '').strip()

        if not age_raw.isdigit() or not (1 <= int(age_raw) <= 120):
            flash('Please enter a valid age between 1 and 120.')
            return render_template('index.html', age=age_raw, ideas=ideas)

        if not ideas:
            flash('Please enter some story ideas.')
            return render_template('index.html', age=age_raw, ideas=ideas)

        if len(ideas) > MAX_IDEAS_LEN:
            flash(f'Ideas must be {MAX_IDEAS_LEN} characters or fewer.')
            return render_template('index.html', age=age_raw, ideas=ideas)

        prompt = (
            f"Write a short story for a {int(age_raw)}-year-old. "
            f"Use these ideas in the story:\n\n{ideas}\n\n"
            f"Start with a title on the first line, then a blank line, then the story."
        )
        story = generate_story(prompt)

        if not story:
            flash('Story generation failed. Is Ollama running?')
            return render_template('index.html', age=age_raw, ideas=ideas)

        lines = story.strip().split('\n')
        title = lines[0].strip() if lines else "Untitled"
        content = '\n'.join(lines[2:]).strip() if len(lines) > 2 else '\n'.join(lines[1:]).strip()

        new_story = Story(user_session=session['session_id'], title=title, content=content)
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('main.stories'))

    return render_template('index.html')

@main.route('/stories')
def stories():
    if 'session_id' not in session:
        return redirect(url_for('main.index'))
    user_stories = Story.query.filter_by(user_session=session['session_id']).order_by(Story.created_at.desc()).all()
    return render_template('stories.html', stories=user_stories)

@main.route('/expand', methods=['GET', 'POST'])
def expand():
    if 'session_id' not in session:
        return redirect(url_for('main.index'))

    user_stories = Story.query.filter_by(user_session=session['session_id']).order_by(Story.created_at.desc()).all()
    selected_story = None
    expanded_content = None

    if request.method == 'POST':
        story_id = request.form.get('story', '').strip()
        ideas = request.form.get('ideas', '').strip()

        if len(ideas) > MAX_IDEAS_LEN:
            flash(f'Ideas must be {MAX_IDEAS_LEN} characters or fewer.')
        elif not story_id or not story_id.isdigit():
            flash('Please select a story to expand.')
        else:
            selected_story = Story.query.filter_by(id=int(story_id), user_session=session['session_id']).first()
            if not selected_story:
                flash('Story not found.')
            else:
                base_prompt = (
                    f"Here is a story:\n\nTitle: {selected_story.title}\n\n{selected_story.content}\n\n"
                    f"Expand this story by adding 3 more paragraphs"
                )
                if ideas:
                    prompt = base_prompt + f". Use these ideas:\n\n{ideas}\n\n"
                else:
                    prompt = base_prompt + " that continue naturally from the last paragraph. "
                prompt += "Only write the 3 new paragraphs. Do not preface your answer with any introduction or explanation."

                new_paragraphs = generate_story(prompt)
                if new_paragraphs:
                    expanded_content = selected_story.content + "\n\n" + new_paragraphs.strip()
                    selected_story.content = expanded_content
                    db.session.commit()
                else:
                    flash('Story expansion failed. Is Ollama running?')
    else:
        story_id = request.args.get('story', '').strip()
        if story_id and story_id.isdigit():
            selected_story = Story.query.filter_by(id=int(story_id), user_session=session['session_id']).first()

    return render_template(
        'expand.html',
        stories=user_stories,
        selected_story=selected_story,
        expanded_content=expanded_content
    )
