from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from functools import wraps
from app.services import facade

admin_ns = Namespace('admin', description='Administrator operations')


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = facade.get_user_by_id(user_id)
        if not user or not user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return wrapper

@api.route('/users/')
class AdminUserResource(Resource):
    @admin_required
    def post(self):
        """
        Admin can create a new user.
        """
        data = request.json
        try:
            new_user = facade.create_user(data)
            return {'message': 'User created', 'user': new_user.to_dict()}, 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/users/<user_id>')
class AdminUserUpdateResource(Resource):
    @admin_required
    def put(self, user_id):
        """
        Admin can update any user.
        """
        data = request.json
        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User updated', 'user': updated_user.to_dict()}, 200


@admin_ns.route('/places/<place_id>')
class AdminPlaceResource(Resource):
    @admin_required
    def put(self, place_id):
        """
        Admin can update any place regardless of ownership.
        """
        data = request.json
        updated_place = facade.update_place(place_id, data)
        if not updated_place:
            return {'error': 'Place not found'}, 404
        return {
            'message': 'Place updated by admin',
            'place': {
                'id': updated_place.id,
                'title': updated_place.title,
                'owner_id': updated_place.owner.id
                # Additional fields as needed
            }
        }, 200
    def delete(self, place_id):
        """
        Admin can delete any place regardless of ownership.
        """
        success = facade.delete_place(place_id)
        if not success:
            return {'error': 'Place not found'}, 404
        return {'message': 'Place deleted by admin'}, 200
    def delete(self, review_id):
        """
        Admin can delete any review regardless of ownership.
        """
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted by admin'}, 200


@admin_ns.route('/amenities/')
class AdminAmenityResource(Resource):
    @admin_required
    def post(self):
        """
        Admin-only creation of an amenity.
        """
        data = request.json
        new_amenity = facade.create_amenity(data)
        return {'message': 'Amenity created', 'amenity': {'id': new_amenity.id, 'name': new_amenity.name}}, 201
