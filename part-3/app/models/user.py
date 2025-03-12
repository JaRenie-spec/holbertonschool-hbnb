import re
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db, bcrypt
from .BaseModel import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relations (si Place et Review sont définis avec une clé étrangère vers User)
    places = db.relationship("Place", backref="owner", lazy=True)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def __init__(self, first_name, last_name, email, is_admin=False):
        # Le constructeur de BaseModel est appelé implicitement
        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first_name (must be non-empty and ≤ 50 characters).")
        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last_name (must be non-empty and ≤ 50 characters).")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.password = None  # Le mot de passe sera défini via hash_password

    def hash_password(self, password):
        """Hash le mot de passe avant de le stocker."""
        self.password = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie le mot de passe fourni par rapport au hash stocké."""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Retourne une représentation dictionnaire de l'utilisateur (sans le mot de passe)."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "places": [p.id for p in self.places] if self.places else [],
            "reviews": [r.id for r in self.reviews] if self.reviews else []
        }
