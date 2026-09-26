from flask import Blueprint, jsonify, request

from src.services.socios.socio_service import (
    create_socio_service,
    get_socio,
    get_socios_service,
    update_socio_service,
)

socio_routes = Blueprint("socios", __name__, url_prefix="/socios")


@socio_routes.route("/<int:socio_id>", methods=["GET"])
def get_socio_route(socio_id):
    socio, error, status = get_socio(socio_id)

    if error:
        return jsonify(error), status

    return jsonify(socio), status


@socio_routes.route("/<int:socio_id>", methods=["PATCH"])
def update_socio_route(socio_id):
    data = request.get_json(silent=True)

    error, status = update_socio_service(socio_id, data)

    if error:
        return jsonify(error), status

    return "", status


@socio_routes.route("", methods=["GET"])
def get_socios_route():
    socios, error, status = get_socios_service(request.base_url, request.args)

    if error:
        return jsonify(error), status

    return jsonify(socios), status


@socio_routes.route("", methods=["POST"])
def create_socio_route():
    data = request.get_json(silent=True)

    error, status = create_socio_service(data)

    if error:
        return jsonify(error), status

    return "", status
