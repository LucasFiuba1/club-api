from flask import Blueprint, jsonify

from src.services.deportes.deporte_service import get_deportes_service

deporte_routes = Blueprint("deportes", __name__, url_prefix="/deportes")


@deporte_routes.route("", methods=["GET"])
def get_deportes_route():
    deportes, error, status = get_deportes_service()

    if error:
        return jsonify(error), status
    return jsonify(deportes), status
