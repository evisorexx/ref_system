from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from referral_system.models.referral_code import ReferralCode
from referral_system.schemas.referral import ReferralCodeCreate, ReferralCodeResponse
from referral_system.database.session import get_db
from referral_system.services.security import get_current_user
from referral_system.models.user import User
from uuid import uuid4

router = APIRouter(prefix="/refcodes", tags=["refcodes"])

@router.post("/create", response_model=ReferralCodeResponse)
async def create_referral_code(
    code_data: ReferralCodeCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать реферальный код.
    """
    existing_code = await db.execute(
        select(ReferralCode)
        .where(ReferralCode.user_id == user.id)
        .where(ReferralCode.is_active)
    )
    if existing_code.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active code",
        )
    
    new_code = ReferralCode(
        code=str(uuid4()),
        expiration_date=code_data.expiration_date,
        user_id=user.id
    )
    db.add(new_code)
    await db.commit()
    await db.close()
    return new_code

@router.delete("/delete/{code_id}")
async def delete_referral_code(
    code_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Удалить реферальный код.
    """
    code = await db.execute(
        select(ReferralCode)
        .where(ReferralCode.id == code_id)
        .where(ReferralCode.user_id == user.id)
    )
    code = code.scalar_one_or_none()
    if not code:
        raise HTTPException(status_code=404, detail="Referral code not found")
    
    await db.delete(code)
    await db.commit()
    await db.close()
    return {"status": "success"}