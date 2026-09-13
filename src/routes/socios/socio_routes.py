from flask import Blueprint, jsonify

from services.socios.socio_service import get_socio

socio_routes = Blueprint("socios", __name__, url_prefix="/socios")


@socio_routes("</int:socio_id>")
def get_socio_route(socio_id):
    socio, error, status = get_socio(socio_id)

    if error:
        return jsonify(error), status

    return jsonify(socio), status
