from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from src.schemas import UserCreate, UserResponse, UserUpdate
from src.database.models import User
from src.database.db import get_db


router = APIRouter(prefix="/users", tags=["users"])

def user_not_found(user_id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"There is no user by id {user_id}")
    
@router.get("/health")
def test():
    return {"message": "test words | prefix: /users"}

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session=Depends(get_db)):
    users = db.query(User).all()  
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_users(user_id: int, db: Session=Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        user_not_found(user_id)
    return user

@router.post("/", response_model=UserResponse)  
def create_user(user: UserCreate, db: Session=Depends(get_db)):
    try:
        new_user = User(**user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error: {e}")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        user_not_found(user_id)
    db.delete(user)
    db.commit()
    return user
    
@router.put("/{user_id}", response_model=UserResponse)
def edit_user(user_id: int, user_new: UserUpdate, db: Session=Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        user_not_found(user_id)
    update_user = user_new.model_dump(exclude_unset=True)
    for attr, new_value in update_user.items():
        setattr(user, attr, new_value)
    db.commit()
    db.refresh(user)
    return user

"""
src/routes/users.py
Завдання: Реалізувати ендпоінти для управління користувачами з прямими запитами до БД усередині функцій.
Деталі:
GET /users/ — отримати список користувачів з пагінацією (skip, limit).
GET /users/{user_id} — отримати профіль конкретного користувача за ID (з обробкою 404 помилки).
POST /users/ — зареєструвати нового користувача з перевіркою на унікальність email та username.
PUT /users/{user_id} — оновити дані профілю користувача.
GET /users/{user_id}/skills — отримати список усіх навичок, якими володіє або цікавиться конкретний користувач.

src/schemas.py
Завдання: Описати Pydantic-моделі для валідації вхідних даних (Create, Update) та серіалізації відповідений (Response).
Деталі:
User: UserBase, UserCreate, UserUpdate, UserResponse.

src/database/models.py
Деталі: Створити базовий клас Base = declarative_base() (або DeclarativeBase) та такі моделі:
User:
id (Integer, Primary Key)
username (String, Unique, Index, не порожнє)
email (String, Unique, Index, не порожнє)
bio (String / Text, опціонально)
created_at (DateTime, автоматичний час створення)
is_active (Boolean, за замовчуванням True)
Зв'язок «багато-до-багато» з навичками (skills).
"""
# Зробити через ШІ
# 1. Доробити решта файлів (exchanges.py, reviews.py)
# 2. Зробити автоматичне тестування (код, який робить запити до вашого API)
