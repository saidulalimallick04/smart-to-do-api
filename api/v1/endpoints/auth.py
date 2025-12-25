from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
import jwt

from core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from models.user import User
from schemas.user import UserCreate, UserOut
from schemas.token import Token, RefreshToken
from core.config import settings
from core.security import ALGORITHM

router = APIRouter()

@router.post("/signup", response_model=UserOut)
async def signup(user_in: UserCreate):
    user = await User.find_one(User.email == user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This Email is already registered"
        )
    
    hashed_password = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name
    )
    await user.insert()
    return user

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(subject=user.email)
    
    return {
        "token_type": "bearer",
        "refresh_token": refresh_token,
        "access_token": access_token
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(token_in: RefreshToken):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = token_in.refresh_token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        type: str = payload.get("type")
        exp: int = payload.get("exp")
        
        if email is None or type != "refresh":
            raise credentials_exception
            
    except jwt.PyJWTError:
        raise credentials_exception
    
    # Check if user exists
    user = await User.find_one(User.email == email)
    if not user:
        raise credentials_exception

    # Generate new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    # Smart Refresh Token Rotation:
    # Only issue a new refresh token if the current one expires in less than 5 days
    
    current_time = datetime.now(timezone.utc)
    expiration_time = datetime.fromtimestamp(exp, tz=timezone.utc)
    remaining_time = expiration_time - current_time
    
    # Calculate a dynamic threshold (e.g., expire_days - 2 days, minimum 1 day)
    rotation_threshold_days = max(1, settings.REFRESH_TOKEN_EXPIRE_DAYS - 2)
    
    if remaining_time < timedelta(days=rotation_threshold_days):
        # Rotate token
        new_refresh_token = create_refresh_token(subject=user.email)
    else:
        # Keep existing token
        new_refresh_token = token
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
