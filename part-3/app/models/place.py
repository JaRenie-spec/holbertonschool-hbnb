from app import db
from .BaseModel import BaseModel
from sqlalchemy import CheckConstraint
from app.models.amenity import place_amenities

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenities, backref='places', lazy='subquery')

    __table_args__ = (
        CheckConstraint("price >= 0", name="price_positive"),
        CheckConstraint("latitude >= -90 AND latitude <= 90", name="latitude_range"),
        CheckConstraint("longitude >= -180 AND longitude <= 180", name="longitude_range"),
    )
