from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx
from app.api.routes import auth, chat, user

app = FastAPI(
    title="CompanionAI", 
    description="AI Companion Chatbot API",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(user.router)

@app.on_event("startup")
async def check_ollama():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("http://localhost:11434/api/tags")
            models = [m["name"] for m in resp.json().get("models", [])]
            print(f"✅ Ollama running. Available models: {models}")
            if "llama3.2" not in " ".join(models):
                print("⚠️  WARNING: llama3.2 model not found. Run: ollama pull llama3.2")
    except Exception as e:
        print(f"❌ Ollama not reachable: {e}. Make sure Ollama is running.")

@app.get("/")
async def root():
    return {"message": "Welcome to CompanionAI API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}