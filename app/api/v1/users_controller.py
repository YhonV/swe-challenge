from uuid import UUID
from fastapi import Response, HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.services.user_service import get_users_services, get_user_by_id, create_user_service, update_user_service, \
    delete_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await get_users_services(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await get_user_by_id(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await create_user_service(db, user)
    if not result:
        raise HTTPException(status_code=409, detail="User already exists")
    return result

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    result = await update_user_service(db, user_id, user)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    result =  await delete_user_service(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")