# ShortStories

A Flask web application that generates and expands age-appropriate short stories for children using a local AI model via [Ollama](https://ollama.com).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation on Linux](#installation-on-linux)
- [Installation on Windows](#installation-on-windows)
- [Installation with Docker Desktop (Windows)](#installation-with-docker-desktop-windows)
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

## Installation with Docker Desktop (Windows)

Docker Desktop bundles Docker Engine and Docker Compose into a single GUI application, making it the easiest way to run the app on Windows without installing Python or Ollama manually.

### 1. Install Docker Desktop

1. Download the installer from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).
2. Run the installer and follow the prompts.
3. When asked, enable **"Use WSL 2 instead of Hyper-V"** (recommended — better performance).
   - If WSL 2 is not already installed, Docker Desktop will prompt you to install it.
4. Restart your computer when prompted.
5. Launch Docker Desktop from the Start menu and wait for the engine to start (the whale icon in the system tray turns solid white).

> **WSL 2 backend requirement:** WSL 2 requires Windows 10 version 2004 (build 19041) or Windows 11. Run `winver` in PowerShell to check your build number.

### 2. Enable WSL 2 (if not already active)

Open PowerShell as Administrator and run:

```powershell
wsl --install
wsl --set-default-version 2
```

Restart your computer, then re-open Docker Desktop. Under **Settings → General**, confirm "Use the WSL 2 based engine" is checked.

### 3. Clone the repository

Open PowerShell:

```powershell
git clone <repository-url> ShortStories
cd ShortStories
```

> If Git is not installed, download it from [git-scm.com](https://git-scm.com/download/win).

### 4. Start the app with Docker Compose

```powershell
docker compose up -d
```

This single command:
- Builds the **ShortStories** app image from the included `Dockerfile`
- Pulls the official **Ollama** image
- Starts both containers and wires them together
- Creates persistent volumes for the database and AI model files

First run will take several minutes while Docker downloads the Ollama image (~1.5 GB). Subsequent starts are instant.

### 5. Pull the AI model

Ollama is now running inside a container but has no model yet. Pull `llama3`:

```powershell
docker exec shortstories-ollama ollama pull llama3
```

This downloads the model into the `ollama_data` Docker volume (~4.7 GB). You only need to do this once.

### 6. Open the app

Navigate to **http://localhost:5000** in your browser.

### Stopping and starting

```powershell
# Stop both containers (data is preserved in volumes)
docker compose down

# Start again
docker compose up -d

# View live logs
docker compose logs -f

# View logs for a single service
docker compose logs -f app
docker compose logs -f ollama
```

### Changing configuration

Create a `.env` file in the project root to override defaults:

```
SECRET_KEY=your-secret-key-here
OLLAMA_MODEL=llama3
```

Then restart:

```powershell
docker compose down && docker compose up -d
```

### Resetting all data

To wipe the database and downloaded models and start fresh:

```powershell
docker compose down -v
```

> **Warning:** `-v` deletes the Docker volumes, including the Ollama model (~4.7 GB). You will need to re-run `ollama pull llama3` afterwards.

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

---

### Docker: containers start but story generation fails

**Symptom:** The app loads but generating a story returns an error.

The `app` container may have started before Ollama finished initializing. Check the Ollama logs:

```powershell
docker compose logs ollama
```

Wait until you see `Listening on 0.0.0.0:11434`, then try again. If the model is missing, pull it:

```powershell
docker exec shortstories-ollama ollama pull llama3
```

---

### Docker: port 5000 already in use

Another process is using port 5000. Either stop that process (see the port conflict section above) or change the host port in `docker-compose.yml`:

```yaml
ports:
  - "5001:5000"   # change 5001 to any free port
```

Then restart: `docker compose down && docker compose up -d` and open **http://localhost:5001**.

---

### Docker: "WSL 2 installation is incomplete"

Open PowerShell as Administrator and run:

```powershell
wsl --update
wsl --set-default-version 2
```

Restart Docker Desktop afterwards.

---

### Docker: image build fails

Ensure Docker Desktop is running (whale icon in system tray), then retry:

```powershell
docker compose build --no-cache
docker compose up -d
```
