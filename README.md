# CompanionAI - AI Companion Chatbot

An AI chatbot that behaves like a caring human companion with memory and emotional intelligence.

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **SQLite** - Database (easy to switch to PostgreSQL)
- **ChromaDB** - Vector database for memory storage
- **Ollama** - Local LLM (llama3.2 for chat, nomic-embed-text for embeddings)
- **JWT** - Authentication

### Frontend
- **React** with Vite
- **Framer Motion** - Animations
- **Axios** - HTTP client

## Project Structure

```
backend/
├── app/
│   ├── api/routes/          # API endpoints
│   │   ├── auth.py          # Register, Login, Refresh token
│   │   ├── chat.py          # Send message, Get history, Clear chat
│   │   └── user.py          # User profile
│   ├── core/
│   │   ├── config.py        # App settings
│   │   ├── database.py      # SQLite setup & models
│   │   └── security.py      # JWT & password hashing
│   ├── models/
│   │   ├── user.py          # Pydantic user models
│   │   └── chat.py          # Pydantic chat models
│   ├── services/
│   │   ├── ai.py            # Ollama chat integration
│   │   └── memory.py        # ChromaDB vector storage
│   └── main.py              # FastAPI app entry point

frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ChatBubble.jsx   # Message bubble
│   │   ├── ChatInput.jsx    # Message input
│   │   ├── Header.jsx       # Chat header
│   │   └── LoadingDots.jsx  # Typing animation
│   ├── pages/
│   │   ├── Login.jsx        # Login page
│   │   ├── Register.jsx     # Register page
│   │   └── Chat.jsx         # Main chat page
│   ├── services/
│   │   └── api.js           # API client
│   └── styles/
│       ├── global.css       # Main styles
│       └── variables.css    # CSS variables
```

## How It Works

### 1. Authentication
- Users register with username, email, password
- Password is hashed using bcrypt
- JWT token is generated and stored on client
- Token is sent in Authorization header for protected routes

### 2. Chat Flow
1. User sends message via `/chat/send` endpoint
2. Backend retrieves conversation history from SQLite
3. Context from ChromaDB (past memories) is fetched
4. Message + history + context sent to Ollama (llama3.2)
5. AI response stored in SQLite and memory
6. Response returned to frontend

### 3. Memory System
- **ChromaDB** stores vector embeddings of conversations
- When user sends a message, similar past memories are retrieved
- These are included in the AI prompt for contextual responses
- This gives the AI "long-term memory"

### 4. Frontend
- Pink/lavender girly theme
- Framer Motion animations for smooth UX
- Messages appear with fade-in effect
- Typing indicator shows while AI is responding

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | User login |
| POST | /chat/send | Send message to AI |
| GET | /chat/history | Get chat history |
| DELETE | /chat/clear | Clear chat history |
| GET | /user/profile | Get user profile |

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama installed with models:
  - `ollama pull llama3.2`
  - `ollama pull nomic-embed-text`

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Backend `.env`:
```
SECRET_KEY=your-secret-key
CHROMA_PERSIST_DIR=./chroma_data
```

## Database

- **SQLite** - `companion_ai.db` (auto-created)
- **ChromaDB** - `./chroma_data/` folder (auto-created)

To switch to PostgreSQL, change `DATABASE_URL` in `backend/app/core/database.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```