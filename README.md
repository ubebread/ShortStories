# ShortStories

A Flask web application that generates and expands age-appropriate short stories for children using a local AI model via [Ollama](https://ollama.com).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation on Linux](#installation-on-linux)
- [Installation on Windows](#installation-on-windows)
- [Running the App](#running-the-app)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Both platforms require the following:

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| pip | bundled with Python 3.10+ | |
| Ollama | latest | [ollama.com](https://ollama.com) — runs the AI model locally |
| llama3 model | — | Downloaded via Ollama (see steps below) |

---

## Installation on Linux

### 1. Install Python

Most Linux distributions ship with Python 3. Verify your version:

```bash
python3 --version
```

If Python 3.10+ is not installed:

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install python3 python3-pip python3-venv -y

# Fedora / RHEL
sudo dnf install python3 python3-pip -y

# Arch
sudo pacman -S python python-pip
```

### 2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start the Ollama service (it runs in the background):

```bash
ollama serve &
```

> On systems with systemd, Ollama may start automatically after install. You can check with `systemctl status ollama`.

Pull the default AI model:

```bash
ollama pull llama3
```

### 3. Clone the repository

```bash
git clone <repository-url> ShortStories
cd ShortStories
```

### 4. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt will change to show `(.venv)` when the environment is active.

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the app

```bash
python run.py
```

Open your browser and navigate to: **http://localhost:5000**

---

## Installation on Windows

### 1. Install Python

Download the latest Python 3.10+ installer from [python.org](https://www.python.org/downloads/windows/).

During installation:
- Check **"Add Python to PATH"** before clicking Install Now.
- Optionally check **"Install pip"** (enabled by default).

Verify in a new Command Prompt or PowerShell window:

```powershell
python --version
pip --version
```

### 2. Install Ollama

Download the Windows installer from [ollama.com/download](https://ollama.com/download).

Run the installer and follow the prompts. Ollama will start automatically in the system tray.

Open a new terminal and pull the default AI model:

```powershell
ollama pull llama3
```

### 3. Clone the repository

```powershell
git clone <repository-url> ShortStories
cd ShortStories
```

> If Git is not installed, download it from [git-scm.com](https://git-scm.com/download/win).

### 4. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Your prompt will change to show `(.venv)` when the environment is active.

### 5. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 6. Run the app

```powershell
python run.py
```

Open your browser and navigate to: **http://localhost:5000**

---

## Running the App

Once started, the server listens on all interfaces at port **5000**:

```
http://localhost:5000
```

To stop the server press `Ctrl+C` in the terminal where it is running.

The SQLite database (`instance/stories.db`) is created automatically on first run — no manual setup required.

---

## Configuration

The app is configured via environment variables. All are optional; defaults work for local development.

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-only-insecure-key-change-in-production` | Flask session secret. **Set this in production.** |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama API endpoint |
| `OLLAMA_MODEL` | `llama3` | Ollama model to use for story generation |

**Linux / macOS — set before running:**

```bash
export SECRET_KEY="your-secret-key-here"
export OLLAMA_MODEL="llama3"
python run.py
```

**Windows PowerShell — set before running:**

```powershell
$env:SECRET_KEY = "your-secret-key-here"
$env:OLLAMA_MODEL = "llama3"
python run.py
```

---

## Usage

The app has three pages:

| Page | URL | Description |
|------|-----|-------------|
| Generate | `/` | Enter a child's age (1–120) and story ideas to generate a new story |
| My Stories | `/stories` | Browse all stories generated in your session |
| Expand | `/expand` | Select an existing story and add 3 new paragraphs to it |

Stories are tracked per browser session — no login required.

---

## Troubleshooting

### Ollama is not running

**Symptom:** Story generation fails or returns an error.

**Fix (Linux):**
```bash
ollama serve &
```

**Fix (Windows):** Open the Ollama app from the Start menu or system tray.

Verify Ollama is reachable:
```bash
curl http://localhost:11434
# Expected: "Ollama is running"
```

---

### `llama3` model not found

**Symptom:** Ollama returns a model-not-found error.

**Fix:**
```bash
ollama pull llama3
```

To use a different model, set `OLLAMA_MODEL` to any model you have pulled (e.g. `mistral`, `phi3`).

---

### Port 5000 already in use

**Linux:**
```bash
# Find the process using port 5000
lsof -i :5000
# Kill it (replace <PID> with the actual PID)
kill <PID>
```

**Windows PowerShell:**
```powershell
netstat -ano | findstr :5000
# Note the PID in the last column, then:
taskkill /PID <PID> /F
```

---

### `ModuleNotFoundError` when running the app

The virtual environment may not be active.

**Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.venv\Scripts\activate
```

Then re-run:
```bash
pip install -r requirements.txt
python run.py
```

---

### Permission denied on Linux when installing Ollama

Run the install script without `sudo` — the installer handles privilege escalation internally. If the issue persists, consult the [Ollama Linux docs](https://github.com/ollama/ollama/blob/main/docs/linux.md).
