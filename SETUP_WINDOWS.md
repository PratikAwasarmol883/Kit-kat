# Running CompanionAI on Windows

A step-by-step guide to run this project locally on Windows.

---

## What You Need to Install First

### 1. Python 3.11
- Go to https://www.python.org/downloads/
- Download **Python 3.11.x** (not 3.12+)
- Run the installer
- **Important:** Check the box that says **"Add Python to PATH"** before clicking Install

Verify it worked — open **Command Prompt** and run:
```
python --version
```
You should see `Python 3.11.x`

---

### 2. Node.js
- Go to https://nodejs.org
- Download the **LTS** version
- Install with default settings

Verify:
```
node --version
npm --version
```

---

### 3. Git
- Go to https://git-scm.com/download/win
- Install with default settings

---

### 4. Ollama (optional — for local AI)
- Go to https://ollama.com/download
- Download and install the Windows version
- After installing, open a new Command Prompt and run:
```
ollama pull gemma3:4b
```
> Skip this if you only want to use the Mistral API (cloud).

---

## Get the Code

Open **Command Prompt** and run:

```
git clone https://github.com/PratikAwasarmol883/Kit-kat.git
cd Kit-kat
```

---

## Set Up the Backend

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Add the API Key

Create a file called `.env` inside the `backend` folder with this content:

```
SECRET_KEY=change-me-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CHROMA_PERSIST_DIR=./chroma_data
MISTRAL_API_KEY=your-mistral-api-key-here
```

> Get a free Mistral API key at https://console.mistral.ai

### Start the Backend

```
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

Leave this window open.

---

## Set Up the Frontend

Open a **new** Command Prompt window:

```
cd Kit-kat\frontend
npm install
npm run dev
```

Leave this window open too.

---

## Open the App

Go to your browser and open:
```
http://localhost:5173
```

---

## Summary — 3 terminals to keep open

| Terminal | Command |
|----------|---------|
| Backend | `cd backend` → `venv\Scripts\activate` → `uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload` |
| Frontend | `cd frontend` → `npm run dev` |
| Ollama (optional) | `ollama serve` |

---

## Common Issues

**`python` not found**
→ Reinstall Python and make sure "Add to PATH" is checked

**`pip install` fails on chromadb**
→ Run this first: `pip install --upgrade pip`

**Port 9000 already in use**
→ Open Task Manager → find the process using port 9000 → end it

**Ollama not responding**
→ Make sure `ollama serve` is running in a separate terminal. The app will automatically fall back to Mistral API if Ollama is not running.
