from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from functools import wraps
from app.services import facade

api = Namespace('admin', description='Admin operations')


# ----------------------
# Models for Swagger UI
# ----------------------
user_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(required=True, description='Is admin user?')
})

amenity_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity')
})


# ----------------------
# Admin check decorator
# ----------------------
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


# -------------------------
# USERS (CREATE / UPDATE)
# -------------------------
@api.route('/users/')
class AdminUserResource(Resource):
    @api.expect(user_model)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid data')
    @api.response(403, 'Admin access required')
    @admin_required
    def post(self):
        """Admin can create a new user."""
        data = request.json
        try:
            new_user = facade.create_user(data)
            return {'message': 'User created', 'user': new_user.to_dict()}, 201
        except Exception as e:
            return {'error': str(e)}, 400


@api.route('/users/<user_id>')
class AdminUserUpdateResource(Resource):
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @admin_required
    def put(self, user_id):
        """Admin can update any user."""
        data = request.json
        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'message': 'User updated', 'user': updated_user.to_dict()}, 200


# -------------------------
# PLACES (UPDATE / DELETE)
# -------------------------
@api.route('/places/<place_id>')
class AdminPlaceResource(Resource):
    @api.expect(api.model('PlaceUpdate', {
        'title': fields.String(description='Title'),
        'description': fields.String(description='Description'),
        'price': fields.Float(description='Price per night'),
        'latitude': fields.Float(description='Latitude'),
        'longitude': fields.Float(description='Longitude'),
        'owner_id': fields.String(description='Owner ID'),
        'amenities': fields.List(fields.String, description='List of amenity IDs')
    }))
    @admin_required
    def put(self, place_id):
        """Admin can update any place regardless of ownership."""
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
            }
        }, 200

    @admin_required
    def delete(self, place_id):
        """Admin can delete any place regardless of ownership."""
        success = facade.delete_place(place_id)
        if not success:
            return {'error': 'Place not found'}, 404
        return {'message': 'Place deleted by admin'}, 200


# -------------------------
# REVIEWS (DELETE)
# -------------------------
@api.route('/reviews/<review_id>')
class AdminReviewResource(Resource):
    @admin_required
    def delete(self, review_id):
        """Admin can delete any review regardless of ownership."""
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted by admin'}, 200


# -------------------------
# AMENITIES (CREATE / UPDATE)
# -------------------------
@api.route('/amenities/')
class AdminAmenityResource(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity created successfully')
    @api.response(403, 'Admin access required')
    @admin_required
    def post(self):
        """Admin-only creation of an amenity."""
        data = request.json
        new_amenity = facade.create_amenity(data)
        return {
            'message': 'Amenity created',
            'amenity': {
                'id': new_amenity.id,
                'name': new_amenity.name
            }
        }, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityUpdateResource(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @admin_required
    def put(self, amenity_id):
        """Admin-only update of an amenity."""
        data = request.json
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'message': 'Amenity updated',
            'amenity': {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }
        }, 200
