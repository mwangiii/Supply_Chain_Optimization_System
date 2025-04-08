from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import uuid
from typing import List, Optional

from supply_chain_backend_fastAPI.core.security import get_password_hash, verify_password, create_access_token
from supply_chain_backend_fastAPI.core.config import settings
from supply_chain_backend_fastAPI.core.database import get_db
from supply_chain_backend_fastAPI.models.users import User
from supply_chain_backend_fastAPI.schemas.users import UserCreate, UserResponse, UserLogin, UserUpdate, Token, TokenData, PasswordChange
from supply_chain_backend_fastAPI.utils.helpers import success_response

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        userid=uuid.uuid4().hex,
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": db_user.userid}
    )
    
    user_data = UserResponse.model_validate(db_user)
    
    return success_response(
        message="User registered successfully",
        data={
            **user_data.model_dump(),
            "jwt_token": access_token
        }
    )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate user
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.userid})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=dict)
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return success_response(
        message="User logged in successfully",
        data={
            "userid": user.userid,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email
        }
    )

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        userid: str = payload.get("sub")
        if userid is None:
            raise credentials_exception
        token_data = TokenData(userid=userid)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.userid == token_data.userid).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/profile", response_model=dict)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return success_response(
        message="User profile retrieved successfully",
        data={
            "userid": current_user.userid,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname,
            "email": current_user.email
        }
    )

@router.put("/profile", response_model=dict)
async def update_user_profile(user_update: UserUpdate, 
                             current_user: User = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    current_user.firstname = user_update.firstname
    current_user.lastname = user_update.lastname
    current_user.email = user_update.email
    
    db.commit()
    db.refresh(current_user)
    
    return success_response(
        message="User profile updated successfully",
        data={
            "userid": current_user.userid,
            "firstname": current_user.firstname,
            "lastname": current_user.lastname,
            "email": current_user.email
        }
    )

@router.put("/password/change", response_model=dict)
async def change_user_password(password_change: PasswordChange,
                              current_user: User = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    if not verify_password(password_change.oldPassword, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid old password"
        )
    
    current_user.password = get_password_hash(password_change.newPassword)
    db.commit()
    
    return success_response(message="User password changed successfully")

@router.get("/")
async def root():
    return {"message": "Welcome to the supply chain management system API!"}