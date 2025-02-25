from BaseModel import BaseModel
class Review(BaseModel):
    def __init__(self, text, rating, user, place):
        super().__init__()
        self.text = text
        self.rating = self.validate_rating(rating)  # Vérification de la note
        self.user = user  # L'utilisateur qui a écrit l'avis
        self.place = place  # La place qui est évaluée

    def validate_rating(self, rating):
        """Vérifie que la note est entre 1 et 5"""
        if not (1 <= rating <= 5):
            raise ValueError("La note doit être entre 1 et 5.")
        return rating
