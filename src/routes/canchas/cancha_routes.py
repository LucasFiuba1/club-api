from flask import Blueprint, jsonify, request
from services.canchas.cancha_service import create_cancha_service

cancha_routes = Blueprint("canchas", __name__, url_prefix="/canchas")

@cancha_routes.post("/")
def create_cancha_route():
    data = request.get_json(silent=True)

    cancha, error, status = create_cancha_service(data)

    if error:
        return jsonify(error), status
    return "", status

    