from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from src.schemas import ExchangeCreate, ExchangeUpdate, ExchangeResponse
from src.database.models import Exchange, User, Skill
from src.database.db import get_db


router = APIRouter(prefix="/exchanges", tags=["exchanges"])


def exchange_not_found(exchange_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"There is no exchange by id {exchange_id}"
    )


@router.get("/", response_model=List[ExchangeResponse])
def get_exchanges(db: Session = Depends(get_db)):
    exchanges = db.scalars(select(Exchange)).all()
    return exchanges


@router.get("/{exchange_id}", response_model=ExchangeResponse)
def get_exchange(exchange_id: int, db: Session = Depends(get_db)):
    exchange = db.get(Exchange, exchange_id)
    if not exchange:
        exchange_not_found(exchange_id)   
    return exchange

@router.post("/", response_model=ExchangeResponse)
def create_exchange(exchange: ExchangeCreate, db: Session = Depends(get_db)):
    new_exchange = Exchange(**exchange.model_dump())
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)
    return new_exchange


@router.put("/{exchange_id}", response_model=ExchangeResponse)
def update_exchange(exchange_id: int, data: ExchangeUpdate, db: Session = Depends(get_db)):
    old_exchange = db.get(Exchange, exchange_id)
    if not old_exchange:
        exchange_not_found(exchange_id)
    pass


@router.get("/my/sent", response_model=List[ExchangeResponse])
def get_my_sent(user_id: int, db: Session = Depends(get_db)):
    exchanges = db.scalars(select(Exchange).where(Exchange.requester_id == user_id)).all()
    return exchanges


@router.get("/my/received", response_model=List[ExchangeResponse])
def get_my_received(user_id: int, db: Session = Depends(get_db)):
    exchanges = db.scalars(select(Exchange).where(Exchange.receiver_id == user_id)).all()
    return exchanges