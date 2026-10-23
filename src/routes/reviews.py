from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List

from src.schemas import ReviewCreate, ReviewResponse
from src.database.models import Review, Exchange, User
from src.database.db import get_db


router = APIRouter(prefix="/reviews", tags=["reviews"])


def review_not_found(review_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"There is no review by id {review_id}"
    )


@router.get("/", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    reviews = db.scalars(select(Review)).all()
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.get(Review, review_id)   
    if not review:
        review_not_found(review_id)      
    return review


@router.post("/", response_model=ReviewResponse)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    new_rewiews = Review(**review.model_dump())
    db.add(new_rewiews)
    db.commit()
    db.refresh(new_rewiews)
    return new_rewiews


@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.reviewed_id == user_id).all()
    return reviews


@router.get("/user/{user_id}/rating")
def get_user_rating(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.reviewed_id == user_id).all()  
    if not reviews:
        return {"user_id": user_id, "rating": 0, "reviews_count": 0}
    average = sum(r.rating for r in reviews) / len(reviews)
    return {
        "user_id": user_id,
        "rating": round(average, 2),
        "reviews_count": len(reviews)
    }