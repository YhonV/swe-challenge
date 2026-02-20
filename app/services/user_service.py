import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


async def get_users_services(db: AsyncSession):
    result = await db.execute(select(User).limit(100))
    return result.scalars().all()

async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user_service(db: AsyncSession, user: UserCreate):
    result: User = await get_user_by_email(db, user.email)
    if result:
        return None

    db_item = User(
        username    = user.username,
        email       = user.email,
        first_name  = user.first_name,
        last_name   = user.last_name,
        role        = user.role,
        active      = True
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def update_user_service(db: AsyncSession, user_id: uuid.UUID, user: UserUpdate):
    result: User = await get_user_by_id(db, user_id)
    if not result:
        return None
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    await db.commit()
    await db.refresh(result)
    return result

async def delete_user_service(db: AsyncSession, user_id: uuid.UUID):
    result: User = await get_user_by_id(db, user_id)
    if not result:
        return None
    await db.delete(result)
    await db.commit()
    return True

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()