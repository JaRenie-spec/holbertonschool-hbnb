from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.user_repository import UserRepository
from app.persistence.repository import SQLAlchemyRepository

class HBnBFacade:
    def __init__(self):
        # Utiliser un repository dédié pour les Users
        self.user_repo = UserRepository()
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # ---------------------- USERS ----------------------
    def create_user(self, user_data):
        # user_data doit contenir first_name, last_name, email, password et éventuellement is_admin
        if self.get_user_by_email(user_data["email"]):
            raise ValueError("This email is already in use.")

        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            is_admin=user_data.get("is_admin", False)
        )
        if "password" not in user_data or not user_data["password"]:
            raise ValueError("Password is required.")
        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "email" in data:
            existing_user = self.get_user_by_email(data["email"])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email is already in use.")
            user.email = data["email"]
        if "password" in data and data["password"]:
            user.hash_password(data["password"])
        if "is_admin" in data:
            user.is_admin = data["is_admin"]

        self.user_repo.update(user_id, user)
        return user

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ---------------------- AMENITIES ----------------------
    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "")
        if not name or len(name) > 50:
            raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
        amenity_obj = Amenity(name=name)
        self.amenity_repo.add(amenity_obj)
        return amenity_obj

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if "name" in data:
            if not data["name"] or len(data["name"]) > 50:
                raise ValueError("Invalid 'name': must be non-empty and ≤ 50 characters.")
            amenity.name = data["name"]
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # ---------------------- PLACES ----------------------
    def create_place(self, place_data):
        if place_data["price"] < 0:
            raise ValueError("Price must be non-negative.")
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")

        place_obj = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        # Relations avec amenities seront ajoutées plus tard
        place_obj.amenities = []
        if "amenities" in place_data:
            for amenity_id in place_data["amenities"]:
                a = self.amenity_repo.get(amenity_id)
                if a:
                    place_obj.amenities.append(a)

        self.place_repo.add(place_obj)
        return place_obj

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "price" in data and data["price"] < 0:
            raise ValueError("Price must be non-negative.")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        if "owner_id" in data:
            new_owner = self.user_repo.get(data["owner_id"])
            if not new_owner:
                raise ValueError("Owner not found.")
            place.owner = new_owner

        if "amenities" in data:
            new_amenities = []
            for amenity_id in data["amenities"]:
                a = self.amenity_repo.get(amenity_id)
                if a:
                    new_amenities.append(a)
            place.amenities = new_amenities

        for field in ["title", "description", "price", "latitude", "longitude"]:
            if field in data:
                setattr(place, field, data[field])

        self.place_repo.update(place_id, place)
        return place

    # ---------------------- REVIEWS ----------------------
    def create_review(self, review_data):
        required = ["text", "rating", "user_id", "place_id"]
        for field in required:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        if not (1 <= review_data["rating"] <= 5):
            raise ValueError("Rating must be between 1 and 5.")

        user = self.user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("User not found.")
        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("Place not found.")

        review_obj = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repo.add(review_obj)
        return review_obj

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        all_reviews = self.review_repo.get_all()
        return [r for r in all_reviews if r.place.id == place_id]

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if "rating" in data:
            if not (1 <= data["rating"] <= 5):
                raise ValueError("Rating must be between 1 and 5.")
        if "text" in data:
            review.text = data["text"]
        if "rating" in data:
            review.rating = data["rating"]
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return self.review_repo.delete(review_id)


# Instanciation globale de la façade
facade = HBnBFacade()
