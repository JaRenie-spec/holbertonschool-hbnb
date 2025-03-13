from app import db
from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError(
                "Invalid 'name': must be non-empty and ≤ 50 characters.")

        self.name = name
