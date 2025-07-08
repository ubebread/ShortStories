# story_writer/app/routes.py
from flask import Blueprint, request, render_template, redirect, session
from .models import db, Story
from .story_engine import generate_story
import uuid
import datetime

main = Blueprint('main', __name__)

def setup(app):
    @app.before_first_request
    def initialize():
        db.create_all()

@main.route('/', methods=['GET', 'POST'])
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    if request.method == 'POST':
        age = request.form['age']
        ideas = request.form['ideas']

        prompt = (
            f"Write a short story for a {age}-year-old. "
            f"The story should include these ideas. "
            f"Start with a title on the first line, then a blank line, then the story: {ideas}"
        )
        story = generate_story(prompt)

        # Extract title and story
        if story:
            lines = story.strip().split('\n')
            title = lines[0].strip() if lines else "Untitled"
            content = '\n'.join(lines[2:]).strip() if len(lines) > 2 else '\n'.join(lines[1:]).strip()
        else:
            title = "Untitled"
            content = ""

        new_story = Story(user_session=session['session_id'], title=title, content=content)
        db.session.add(new_story)
        db.session.commit()
        return redirect('/stories')

    return render_template('index.html')

@main.route('/stories')
def stories():
    user_stories = Story.query.filter_by(user_session=session['session_id']).all()
    return render_template('stories.html', stories=user_stories)

@main.route('/expand', methods=['GET', 'POST'])
def expand():
    stories = Story.query.filter_by(user_session=session['session_id']).all()
    selected_story = None
    expanded_content = None

    if request.method == 'POST':
        story_id = request.form.get('story')
        ideas = request.form.get('ideas')
        if story_id:
            selected_story = Story.query.filter_by(id=story_id, user_session=session['session_id']).first()
            if selected_story and ideas:
                # Prompt for expansion
                prompt = (
                    f"Here is a story:\n\nTitle: {selected_story.title}\n\n{selected_story.content}\n\n"
                    f"Expand this story by adding 3 more paragraphs. Use these ideas for expansion: {ideas}\n"
                    f"Only write the 3 new paragraphs."
                )
                new_paragraphs = generate_story(prompt)  # Your AI function
                # Append new paragraphs to the original content
                expanded_content = selected_story.content + "\n\n" + new_paragraphs.strip()
                # Overwrite the original story content with the expanded content
                selected_story.content = expanded_content
                db.session.commit()
    else:
        story_id = request.args.get('story')
        if story_id:
            selected_story = Story.query.filter_by(id=story_id, user_session=session['session_id']).first()

    return render_template(
        'expand.html',
        stories=stories,
        selected_story=selected_story,
        expanded_content=expanded_content
    )