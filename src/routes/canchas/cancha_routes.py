from flask import Blueprint, jsonify, request
from services.canchas.cancha_service import create_cancha_service, patch_cancha_service, delete_cancha_service

cancha_routes = Blueprint("canchas", __name__, url_prefix="/canchas")

@cancha_routes.post("/")
def create_cancha_route():
    data = request.get_json(silent=True)

    cancha, error, status = create_cancha_service(data)

    if error:
        return jsonify(error), status
    return "", status

@cancha_routes.patch("/<int:id_cancha>")
def patch_cancha_route(id_cancha):
    data = request.get_json(silent=True)

    error, status = patch_cancha_service(id_cancha, data)

    if error:
        return jsonify(error), status
    return "", status

@cancha_routes.delete("/<int:id_cancha>")
def delete_cancha_route(id_cancha):

    error, status = delete_cancha_service(id_cancha)

    if error:
        return jsonify(error), status
    return "", status

