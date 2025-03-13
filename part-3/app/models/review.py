from app import db
from .BaseModel import BaseModel
from sqlalchemy import CheckConstraint

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range"),
    )
