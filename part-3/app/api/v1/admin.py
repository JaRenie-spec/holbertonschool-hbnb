from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from functools import wraps
from app.services import facade

admin_ns = Namespace('admin', description='Administrator operations')


def admin_required(fn):
    """Decorator to ensure the user is an admin."""
    from flask_jwt_extended import get_jwt_identity

    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        return fn(*args, **kwargs)
    return jwt_required()(wraps(fn)(wrapper))


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
