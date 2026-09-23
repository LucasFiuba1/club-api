from flask import Blueprint, jsonify, request

from services.canchas.cancha_service import get_canchas_disponibles_service
from validators.cancha_validator import validate_disponibilidad
from utils.error_utils import build_error

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