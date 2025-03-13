from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from functools import wraps
from app.services import facade

api = Namespace('admin', description='Admin operations')


def admin_required(fn):
    """
    Decorator to ensure the current user has admin privileges.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return wrapper


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, user_id):
        """
        Update any user's details (ADMIN ONLY).
        """
        data = request.json
        if 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and str(existing_user.id) != str(user_id):
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'message': 'User updated successfully',
                'user': updated_user.to_dict()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @jwt_required()
    @admin_required
    def delete(self, user_id):
        """
        Delete any user account (ADMIN ONLY).
        """
        deleted_user = facade.delete_user(user_id)
        if not deleted_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200


@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        """
        Create a new user (ADMIN ONLY).
        The admin can set is_admin to True or False as needed.
        """
        data = request.json
        if 'email' not in data or 'password' not in data:
            return {'error': 'Missing email or password'}, 400

        if facade.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            user = facade.create_user(data)
            return {
                'message': 'User created',
                'user': user.to_dict()
            }, 201
        except Exception as e:
            return {'error': str(e)}, 500
