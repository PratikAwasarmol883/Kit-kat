from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json
from app.models.chat import ChatRequest, ChatResponse, ChatHistoryResponse, Message
from app.core.database import get_db, User, Conversation
from app.core.security import get_current_user
from app.services.ai import get_ai_response, detect_tone
from app.services.memory import store_memory, retrieve_memories

router = APIRouter(prefix="/chat", tags=["chat"])

def get_user_name(user_id: str, db: Session) -> str:
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user:
        prefs = json.loads(user.preferences or "{}")
        return prefs.get("name", user.username)
    return "User"

def get_or_create_conversation(user_id: str, db: Session):
    conv = db.query(Conversation).filter(Conversation.user_id == int(user_id)).first()
    if not conv:
        conv = Conversation(
            user_id=int(user_id),
            messages="[]"
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)
    return conv

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = get_or_create_conversation(user_id, db)
    
    messages = json.loads(conv.messages or "[]")
    
    # Build history for AI (last 5 messages)
    history = []
    for msg in messages[-5:]:
        history.append({
            "role": "user" if msg.get("role") == "user" else "assistant",
            "content": msg.get("content", "")
        })
    
    # Get AI response
    ai_reply = await get_ai_response(
        user_message=request.message,
        conversation_history=history
    )
    
    timestamp = datetime.utcnow()
    
    user_msg = {
        "role": "user",
        "content": request.message,
        "timestamp": timestamp.isoformat()
    }
    
    ai_msg = {
        "role": "assistant",
        "content": ai_reply,
        "timestamp": timestamp.isoformat()
    }
    
    messages = messages + [user_msg, ai_msg]
    conv.messages = json.dumps(messages)
    conv.updated_at = timestamp
    db.commit()
    
    # Store important messages in memory
    if len(request.message) > 20:
        store_memory(user_id, f"User mentioned: {request.message[:100]}")
    if len(ai_reply) > 20:
        store_memory(user_id, f"AI said: {ai_reply[:100]}")
    
    return ChatResponse(reply=ai_reply, timestamp=timestamp)

@router.get("/history", response_model=ChatHistoryResponse)
async def get_history(limit: int = 50, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = get_or_create_conversation(user_id, db)
    messages = json.loads(conv.messages or "[]")[-limit:]
    return ChatHistoryResponse(messages=[Message(**m) for m in messages])

@router.delete("/clear")
async def clear_chat(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = get_or_create_conversation(user_id, db)
    conv.messages = "[]"
    conv.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Chat cleared"}