from flask import Blueprint, jsonify, request

from src.services.canchas.cancha_service import (
    create_cancha_service,
    delete_cancha_service,
    get_cancha_service,
    get_canchas_disponibles_service,
    get_canchas_service,
    patch_cancha_service,
)
from utils.error_utils import build_error
from validators.cancha_validator import validate_disponibilidad

cancha_routes = Blueprint("canchas", __name__, url_prefix="/canchas")

@cancha_routes.route("/disponibles", methods=["GET"])
def get_canchas_disponibles_route():
    fecha = request.args.get("fecha")
    hora_inicio = request.args.get("hora_inicio")
    hora_fin = request.args.get("hora_fin")
    id_deporte = request.args.get("id_deporte")
    techada = request.args.get("techada")

    if id_deporte is not None:
        id_deporte=int(id_deporte)
    if techada is not None:
        techada=techada.lower()=="true"

    data={"fecha": fecha, 
          "hora_inicio": hora_inicio, 
          "hora_fin": hora_fin, 
          "id_deporte": id_deporte, 
          "techada": techada
    }
    es_valido, error_validacion = validate_disponibilidad(data)
    if not es_valido:
        error = build_error("DATOS_INVALIDOS", "Datos inválidos.", error_validacion)
        return jsonify(error), 400

    canchas, error, status = get_canchas_disponibles_service(fecha, hora_inicio, hora_fin, id_deporte, techada)

    if error:
        return jsonify(error), status
    if not canchas:
        return "", 204
    
    return jsonify({"canchas": canchas}), status


@cancha_routes.get("/<int:cancha_id>", METHODS=['GET'])
def get_cancha_route(cancha_id):
    cancha, error, status = get_cancha_service(cancha_id)

    if error:
        return jsonify(error), status

    return jsonify(cancha), status


@cancha_routes.get("")
def get_canchas_route():
    canchas, error, status = get_canchas_service(
        request.base_url,
        request.args
    )

    if error:
        return jsonify(error), status

    return jsonify(canchas), status


@cancha_routes.post("")
def create_cancha_route():
    data = request.get_json(silent=True)

    _, error, status = create_cancha_service(data)

    if error:
        return jsonify(error), status

    return "", status


@cancha_routes.patch("/<int:id_cancha>", METHODS=['PATCH'])
def patch_cancha_route(id_cancha):
    data = request.get_json(silent=True)

    error, status = patch_cancha_service(id_cancha, data)

    if error:
        return jsonify(error), status

    return "", status


@cancha_routes.delete("/<int:id_cancha>", METHODS = ['DELETE'])
def delete_cancha_route(id_cancha):
    error, status = delete_cancha_service(id_cancha)

    if error:
        return jsonify(error), status

    return "", status
