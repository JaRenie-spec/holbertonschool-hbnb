from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

places_ns = Namespace('places', description='Public Place operations')

amenity_model = places_ns.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = places_ns.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = places_ns.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@places_ns.route('/')
class PlaceList(Resource):
    @places_ns.expect(place_model)
    @places_ns.response(201, 'Place successfully created')
    @places_ns.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new place.
        - A normal user can specify owner_id, but ideally it should match the current user's ID.
        - This endpoint remains as it was before.
        """
        place_data = request.json
        try:
            place_obj = facade.create_place(place_data)
            return {
                "id": place_obj.id,
                "title": place_obj.title,
                "description": place_obj.description,
                "price": place_obj.price,
                "latitude": place_obj.latitude,
                "longitude": place_obj.longitude,
                "owner_id": place_obj.owner.id,
                "owner": {
                    "id": place_obj.owner.id,
                    "first_name": place_obj.owner.first_name,
                    "last_name": place_obj.owner.last_name,
                    "email": place_obj.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in place_obj.amenities]
            }, 201
        except ValueError as e:
            return {"message": str(e)}, 400

    def get(self):
        """
        Retrieve a list of all places, including owner and amenities information.
        """
        places = facade.get_all_places()
        result = []
        for p in places:
            result.append({
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id,
                "owner": {
                    "id": p.owner.id,
                    "first_name": p.owner.first_name,
                    "last_name": p.owner.last_name,
                    "email": p.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in p.amenities]
            })
        return result, 200


@places_ns.route('/<place_id>')
class PlaceResource(Resource):
    @places_ns.response(200, 'Place details retrieved successfully')
    @places_ns.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve details of a place by its ID.
        """
        try:
            p = facade.get_place(place_id)
            return {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "latitude": p.latitude,
                "longitude": p.longitude,
                "owner_id": p.owner.id,
                "owner": {
                    "id": p.owner.id,
                    "first_name": p.owner.first_name,
                    "last_name": p.owner.last_name,
                    "email": p.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in p.amenities]
            }, 200
        except ValueError:
            return {"message": "Place not found"}, 404

    @places_ns.expect(place_model)
    @places_ns.response(200, 'Place updated successfully')
    @places_ns.response(400, 'Invalid input data')
    @places_ns.response(404, 'Place not found')
    def put(self, place_id):
        """
        Update a place's information.
        This endpoint remains as before. Any logic for authentication can be added as needed.
        """
        place_data = request.json
        try:
            updated = facade.update_place(place_id, place_data)
            if not updated:
                return {"message": "Place not found"}, 404
            return {
                "id": updated.id,
                "title": updated.title,
                "description": updated.description,
                "price": updated.price,
                "latitude": updated.latitude,
                "longitude": updated.longitude,
                "owner_id": updated.owner.id,
                "owner": {
                    "id": updated.owner.id,
                    "first_name": updated.owner.first_name,
                    "last_name": updated.owner.last_name,
                    "email": updated.owner.email
                },
                "amenities": [{"id": a.id, "name": a.name} for a in updated.amenities]
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": f"An error occurred: {e}"}, 500
