from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from referral_system.database.session import get_db
from referral_system.models.user import User
from referral_system.models.referral_code import ReferralCode
from referral_system.schemas.auth import UserCreate, Token
from referral_system.services.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Регистрация нового пользователя.
    """
    existing_user = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    hashed_password = get_password_hash(user_data.password)
    exec_ref_id = await db.execute(
        select(ReferralCode.user_id).where(ReferralCode.code == user_data.referral_code)
    )
    ref_id = exec_ref_id.scalar_one_or_none()
    new_user = User(email=user_data.email, hashed_password=hashed_password, referrer_id=ref_id)
    db.add(new_user)
    await db.commit()
    await db.close()
        
    access_token = create_access_token({"sub": new_user.email})
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Прохождение аутентификации.
    """
    user = await db.execute(select(User).where(User.email == form_data.username))
    user = user.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}