from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        # Remplacement du repository en mémoire par SQLAlchemyRepository
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def _user_to_dict(self, user_obj):
        if not user_obj:
            return None
        return {
            "id": user_obj.id,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "email": user_obj.email
        }

    def _amenity_to_dict(self, amenity_obj):
        if not amenity_obj:
            return None
        return {
            "id": amenity_obj.id,
            "name": amenity_obj.name
        }

    def _place_to_dict(self, place_obj):
        if not place_obj:
            return None
        return {
            "id": place_obj.id,
            "title": place_obj.title,
            "description": place_obj.description,
            "price": place_obj.price,
            "latitude": place_obj.latitude,
            "longitude": place_obj.longitude,
            "owner_id": place_obj.owner.id,
            "amenities": [a.id for a in place_obj.amenities] if hasattr(place_obj, "amenities") else []
        }

    def _review_to_dict(self, review_obj):
        if not review_obj:
            return None
        return {
            "id": review_obj.id,
            "text": review_obj.text,
            "rating": review_obj.rating,
            "user_id": review_obj.user.id,
            "place_id": review_obj.place.id
        }

    def create_user(self, user_data):
        existing = self.get_user_by_email(user_data["email"])
        if existing:
            raise ValueError("This email is already in use.")

        user_obj = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"]
        )
        if "password" not in user_data or not user_data["password"]:
            raise ValueError("Password is required.")
        user_obj.hash_password(user_data["password"])

        self.user_repo.add(user_obj)
        return user_obj

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, data):
        return self.user_repo.update(user_id, data)

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

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
        amenity.update(data)
        self.amenity_repo.add(amenity)
        return amenity

    def create_place(self, place_data):
        if place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
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
        place_obj.amenities = [] if not hasattr(place_obj, "amenities") else place_obj.amenities

        if "amenities" in place_data:
            amenities = []
            for amenity_id in place_data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    amenities.append(amenity_obj)
            place_obj.amenities = amenities

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
            raise ValueError("Price must be a non-negative value.")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        if "owner_id" in data:
            new_owner = self.user_repo.get(data["owner_id"])
            if not new_owner:
                raise ValueError("Owner not found.")
            place.owner = new_owner
            data.pop("owner_id")

        if "amenities" in data:
            new_amenities = []
            for amenity_id in data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    new_amenities.append(amenity_obj)
            place.amenities = new_amenities
            data.pop("amenities")

        place.update(data)
        self.place_repo.add(place)
        return place

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
        review.update(data)
        self.review_repo.add(review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return self.review_repo.delete(review_id)
