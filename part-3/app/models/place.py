from app import db
from app.models.BaseModel import BaseModel

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
                         db.Column('place_id', db.Integer, db.ForeignKey(
                             'places.id'), primary_key=True),
                         db.Column('amenity_id', db.Integer, db.ForeignKey(
                             'amenities.id'), primary_key=True)
                         )


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, lazy='subquery',
                                backref=db.backref('places', lazy=True))

    """
    Place class.
    Attributes:
      - id (from BaseModel)
      - title: Required, max 100 characters
      - description: Optional
      - price: Float, must be positive
      - latitude: Must be between -90 and 90
      - longitude: Must be between -180 and 180
      - owner: User who owns the place
      - reviews: List of associated reviews
      - amenities: List of associated amenities

    Validation:
      - title must be non-empty and ≤ 100 characters
      - price must be >= 0
      - latitude must be in range [-90, 90]
      - longitude must be in range [-180, 180]
    """

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError(
                "Invalid 'title': must be non-empty and ≤ 100 characters.")

        if price < 0:
            raise ValueError("Invalid 'price': must be a positive number.")

        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid 'latitude': must be between -90 and 90.")

        if not (-180 <= longitude <= 180):
            raise ValueError(
                "Invalid 'longitude': must be between -180 and 180.")

        from .user import User
        if not isinstance(owner, User):
            raise TypeError("Expected 'owner' to be an instance of User.")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner.id

    def add_review(self, review):
        """Adds a Review to the Place."""
        from .review import Review
        if not isinstance(review, Review):
            raise TypeError("Expected 'review' to be an instance of Review.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an Amenity to the Place."""
        from .amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Expected 'amenity' to be an instance of Amenity.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
