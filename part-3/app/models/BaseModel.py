import uuid
from datetime import datetime, timezone
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # Empêche la création d'une table pour BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)  # Date/heure "timezone-aware" en UTC
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def save(self):
        """
        Met à jour le timestamp 'updated_at' lorsqu'un objet est modifié.
        """
        self.updated_at = datetime.now(timezone.utc)

    def update(self, data: dict):
        """
        Met à jour les attributs de l'objet à partir d'un dictionnaire
        et rafraîchit le timestamp 'updated_at'.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
