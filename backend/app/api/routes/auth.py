from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.core.database import get_db, User
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        preferences='{"name": "' + user_data.username + '"}'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    token = create_access_token({"sub": str(user.id)})
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(user.id)})
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            created_at=user.created_at
        )
    )

@router.post("/refresh")
async def refresh_token(user_id: str = Depends(get_current_user)):
    token = create_access_token({"sub": user_id})
    return {"access_token": token, "token_type": "bearer"}