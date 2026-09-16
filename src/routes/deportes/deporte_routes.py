from flask import Blueprint, jsonify, request

from services.canchas.cancha_service import get_deportes_service

deporte_routes = Blueprint("deportes", __name__, url_prefix="/deportes")


@deporte_routes.get("")
def get_deportes_route():
    deportes, error, status = get_deportes_service()

    if error:
        return jsonify(error), status
    return jsonify(deportes), status
