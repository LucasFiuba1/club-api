from flask import Blueprint, jsonify, request

from services.canchas.cancha_service import get_cancha_service, get_canchas_service

cancha_routes = Blueprint("canchas", __name__, url_prefix="/canchas")


@cancha_routes.get("/<cancha_id>")
def get_cancha_route(cancha_id):

    cancha, error, status = get_cancha_service(cancha_id)

    if error:
        return jsonify(error), status

    return jsonify(cancha), status

@cancha_routes.get("")
def get_canchas_route():

    canchas, error, status = get_canchas_service(request.base_url, request.args)

    if error:
        return jsonify(error), status
    return jsonify(canchas), status


