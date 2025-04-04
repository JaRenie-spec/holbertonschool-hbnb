from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt,
    jwt_required, get_jwt_identity
)
from flask import request
from app.services import facade
from app.extensions import jwt_blacklist  # Assure-toi que ce set est bien initialisé quelque part dans extensions.py

api = Namespace('auth', description='Authentication operations')

# --------------------
# Models
# --------------------
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

# --------------------
# Login
# --------------------
@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """
        User login.
        """
        login_data = api.payload
        user = facade.get_user_by_email(login_data['email'])
        if user and user.verify_password(login_data['password']):
            access_token = create_access_token(identity={'id': user.id, 'is_admin': user.is_admin})
            refresh_token = create_refresh_token(identity={'id': user.id, 'is_admin': user.is_admin})
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'token_type': 'Bearer',# Indique le type de token
                'refresh_token': refresh_token,
                'user_id': user.id,
                'is_admin': user.is_admin
            }, 200
        return {'message': 'Invalid credentials'}, 401


# --------------------
# Refresh Token
# --------------------
#@api.route('/refresh')
#class RefreshToken(Resource):
#    @jwt_required(refresh=True)
#    def post(self):
#        identity = get_jwt_identity()
#        new_access_token = create_access_token(identity=identity)
#        return {'access_token': new_access_token}, 200


# --------------------
# Logout
# --------------------
@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        jwt_blacklist.add(jti)
        return {'message': 'Successfully logged out'}, 200

# --------------------
# Protected Endpoint
# --------------------
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user_id = identity.get('id')
        is_admin = identity.get('is_admin')
        return {
            'message': f'Hello user {user_id}',
            'is_admin': is_admin
        }, 200
