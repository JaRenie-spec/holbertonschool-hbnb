from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

auth_ns = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = auth_ns.payload  # Get email and password from the request payload

        # Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity={'id': str(user.id), 'is_admin': user.is_admin})
        return {'access_token': access_token}, 200


@auth_ns.route('/protected')
class ProtectedResource(Resource):
    @auth_ns.doc(security='Bearer')
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user["id"]}'}, 200
