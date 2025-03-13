import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from dotenv import load_dotenv
from config import config

# Extensions globales (pas encore attachées à l'app)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

# Configuration Swagger / Restx
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Enter 'Bearer <JWT>'"
    }
}

def create_app(config_name='default'):
    """
    Application Factory : crée et configure l'application Flask,
    initialise les extensions et enregistre les namespaces de l'API.
    """
    # Charger les variables d'environnement depuis .env si présent
    load_dotenv()

    # Créer l'application Flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

<<<<<<< HEAD
    # Exemple : définir la clé JWT si vous le souhaitez explicitement
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'my_flask_session_key')
=======
    # Import and register namespaces here to avoid circular imports
    from app.api.v1.users import api as users_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.admin import api as admin_ns
>>>>>>> ee5466782dcb4dc2513c2106450f0b1aaf852fdd

    # ---- Importer les namespaces APRÈS la création de l'app ----
    from app.api.v1.users import users_ns
    from app.api.v1.places import places_ns
    from app.api.v1.reviews import reviews_ns
    from app.api.v1.amenities import amenities_ns
    from app.api.v1.auth import auth_ns
    from app.api.v1.admin import admin_ns

    # Créer l'instance de l'API Flask-Restx
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        authorizations=authorizations,
        security='Bearer'
    )

    # Enregistrer les différents namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')
<<<<<<< HEAD

=======
>>>>>>> ee5466782dcb4dc2513c2106450f0b1aaf852fdd
    return app
