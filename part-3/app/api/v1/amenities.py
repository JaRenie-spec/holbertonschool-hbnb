from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

amenities_ns = Namespace('amenities', description='Amenity operations')

amenity_model = amenities_ns.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@amenities_ns.route('/')
class AmenityList(Resource):
    @amenities_ns.expect(amenity_model, validate=True)
    @amenities_ns.response(201, 'Amenity successfully created')
    @amenities_ns.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Create a new amenity.
        Any authenticated user can do this.
        (If you want it fully public, remove @jwt_required().)
        """
        current_user = get_jwt_identity()
        # We do not check is_admin here, so normal users can create amenities.
        amenity_data = amenities_ns.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @amenities_ns.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve all amenities.
        This endpoint is open to everyone.
        """
        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name
            }
            for a in amenities
        ], 200

@amenities_ns.route('/<amenity_id>')
class AmenityResource(Resource):
    @amenities_ns.response(200, 'Amenity details retrieved successfully')
    @amenities_ns.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get details of an amenity by its ID.
        Open to everyone.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @amenities_ns.expect(amenity_model)
    @amenities_ns.response(200, 'Amenity updated successfully')
    @amenities_ns.response(404, 'Amenity not found')
    @amenities_ns.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, amenity_id):
        """
        Update an amenity's information.
        Any authenticated user can do this.
        (Remove @jwt_required() if you want it fully open.)
        """
        current_user = get_jwt_identity()
        # No is_admin check => normal users can update amenities as well.
        amenity_data = amenities_ns.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400
