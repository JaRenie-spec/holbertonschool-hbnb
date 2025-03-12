# app/routes.py
from flask import Blueprint, request, jsonify
from app.services.facade import facade

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = facade.create_user(data)
    return jsonify(user.to_dict()), 201
