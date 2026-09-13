from flask import Blueprint, jsonify, request

from services.socios.socio_service import get_socio, update_socio_service

socio_routes = Blueprint("socios", __name__, url_prefix="/socios")


@socio_routes("</int:socio_id>")
def get_socio_route(socio_id):
    socio, error, status = get_socio(socio_id)

    if error:
        return jsonify(error), status

    return jsonify(socio), status

@socio_routes("</int:socio_id>")
def update_socio_route(socio_id):
    data = request.get_json(silent=True)

    socio, error, status = update_socio_service(socio_id, data)

    if error:
        return jsonify(error), status

    return jsonify(socio), status
