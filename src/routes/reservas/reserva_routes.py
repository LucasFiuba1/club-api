from flask import Blueprint, jsonify, request

from src.services.reservas.reserva_service import create_reserva_service
from src.utils.error_utils import build_error
from src.validators.reserva_validator import validate_reserva

reserva_routes=Blueprint("reservas", __name__, url_prefix="/reservas")

@reserva_routes.route("/", methods=["POST"])
def create_reserva_route():
    data = request.get_json()

    es_valida, error_validacion = validate_reserva(data)

    if not es_valida:
        error = build_error("DATOS_INVALIDOS", "Datos inválidos", error_validacion)
        return jsonify(error), 400

    reserva, error, status = create_reserva_service(
        data["id_socio"], data["id_cancha"], data["fecha_hora_inicio"], data["fecha_hora_fin"]
    )

    if error:
        return jsonify(error), status

    return jsonify(reserva), status