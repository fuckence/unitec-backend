from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db import get_db
from app.models.user import User
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/test", tags=["test"])

class UserCreate(BaseModel):
    aitu_user_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    go: Optional[str] = None
    region: Optional[str] = None
    raion: Optional[str] = None
    office_number: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseModel):
    aitu_user_id: str
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    go: Optional[str]
    region: Optional[str]
    raion: Optional[str]
    office_number: Optional[str]
    phone: Optional[str]
    
    class Config:
        from_attributes = True

@router.get("/db-connection")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "status": "success",
            "message": "Database connection successful",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

@router.get("/db-info")
async def get_db_info(db: Session = Depends(get_db)):
    try:
        version = db.execute(text("SELECT VERSION()")).scalar()
        database = db.execute(text("SELECT DATABASE()")).scalar()
        user_count = db.query(User).count()
        
        return {
            "mysql_version": version,
            "database": database,
            "users_count": user_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-user", response_model=UserResponse)
async def create_test_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.aitu_user_id == user_data.aitu_user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        user = User(**user_data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{aitu_user_id}", response_model=UserResponse)
async def get_user(aitu_user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.aitu_user_id == aitu_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/user/{aitu_user_id}")
async def delete_user(aitu_user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.aitu_user_id == aitu_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": f"User {aitu_user_id} deleted successfully"}

@router.delete("/users/all")
async def delete_all_users(db: Session = Depends(get_db)):
    try:
        count = db.query(User).count()
        db.query(User).delete()
        db.commit()
        return {"message": f"Deleted {count} users"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))