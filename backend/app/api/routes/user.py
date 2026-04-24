from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import UserResponse, UserProfile, UserPreferences
from app.core.database import get_db, User
from app.core.security import get_current_user
import json

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=UserResponse)
async def get_profile(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        created_at=user.created_at
    )

@router.put("/profile")
async def update_profile(profile: UserProfile, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == int(user_id)).first()
    if profile.preferences:
        user.preferences = json.dumps(profile.preferences.dict())
        db.commit()
    return {"message": "Profile updated"}