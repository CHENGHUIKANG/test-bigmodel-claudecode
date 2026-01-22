from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.session import UserSession
from schemas.user import (
    UserCreate, UserResponse, UserUpdate, UserLogin,
    Token, TokenData
)
from utils import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token,
    verify_token
)
from config import settings

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否已存在
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )

    # 创建新用户
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        bio=user.bio,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账号已被禁用"
        )

    # 生成token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})

    # 保存会话信息
    db_session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        access_token=access_token,
        expires_at=datetime.utcnow() + timedelta(days=7)
    )
    db.add(db_session)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    username = token_data.get("username")

    user = db.query(User).filter(User.username == username).first()
    if user:
        # 使所有该用户的会话失效
        db.query(UserSession).filter(
            UserSession.user_id == user.id,
            UserSession.is_active == True
        ).update({"is_active": False})
        db.commit()

    return {"message": "登出成功"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    username = token_data.get("username")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token_data = verify_token(credentials.credentials)
    username = token_data.get("username")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 更新用户信息
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

@router.get("/profile/{username}", response_model=UserResponse)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    return user