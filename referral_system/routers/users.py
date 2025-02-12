from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from referral_system.database.session import AsyncSessionLocal
from referral_system.models.user import User
from referral_system.schemas.auth import UserCreate
from referral_system.services.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserCreate)
async def user_page(
    current_user: User = Depends(get_current_user)
):
    """
    Получить информацию о текущем пользователе.
    """
    return {
        "email": current_user.email,
        # Пароль не возвращаем, так как это чувствительная информация
    }

@router.put("/me/email")
async def update_user_email(
    new_email: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(AsyncSessionLocal)
):
    """
    Обновить email текущего пользователя.
    """
    existing_user = await db.execute(select(User).where(User.email == new_email))
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    current_user.email = new_email
    await db.commit()
    return {"message": "Email updated successfully"}

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(AsyncSessionLocal)
):
    """
    Удалить текущего пользователя.
    """
    await db.delete(current_user)
    await db.commit()
    return None  # 204 No Content