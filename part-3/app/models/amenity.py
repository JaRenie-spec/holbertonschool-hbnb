from app import db
from app.models.BaseModel import BaseModel
from sqlalchemy import Table, Column, ForeignKey

# Association table for Place-Amenity many-to-many relationship
place_amenities = db.Table('place_amenities',
    Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    places = db.relationship('Place', secondary=place_amenities, backref='amenities', lazy='subquery')
