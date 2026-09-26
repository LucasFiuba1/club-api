from flask import Blueprint, jsonify, request

from src.services.reservas.reserva_service import (
    cambiar_estado_reserva,
    create_reserva_service,
    listar_reservas,
    obtener_reserva,
)
from src.utils.error_utils import build_error
from src.validators.reserva_validator import validate_reserva

reserva_routes=Blueprint("reservas", __name__, url_prefix="/reservas")

@reserva_routes.route('/reservas', methods=['GET'])
def get_reserva():

    limit = int(request.args.get('_limit', 10))
    offset = int(request.args.get('_offset', 0))

    filters = {
        'id_cancha': request.args.get('id_cancha'),
        'id_socio': request.args.get('id_socio'),
        'estado': request.args.get('estado'),
        'fecha_desde': request.args.get('fecha_desde'),
        'fecha_hasta': request.args.get('fecha_hasta')
    }

    reservas, total = listar_reservas(filters, limit, offset)

    links = {
        "_first": f"/reservas?_limit={limit}&_offset=0",
        "_prev": f"/reservas?_limit={limit}&_offset={max(0, offset - limit)}" if offset > 0 else None,
        "_next": f"/reservas?_limit={limit}&_offset={offset + limit}" if offset + limit < total else None,
        "_last": f"/reservas?_limit={limit}&_offset={max(0, total - limit)}"
    }

    return jsonify({
        'reservas': reservas,
        '_links': links
    }), 200


@reserva_routes.route('/reservas/<int:reserva_id>', methods=['GET'])
def get_reserva_by_id(reserva_id):
    reserva = obtener_reserva(reserva_id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404

    return jsonify(reserva), 200

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


@reserva_routes.route('/reservas/<int:reserva_id>/estado', methods=['PUT'])
def update_estado(reserva_id):
    """
    Endpoint paraactualizar el estado de una reserva por su ID
    """
    data = request.get_json()

    if not data or 'estado' not in data:
        return jsonify({'error': 'El campo estado es obligatorio'}), 400

    resultado = cambiar_estado_reserva(reserva_id, data['estado'])

    if 'error' in resultado:
        return jsonify({'error': resultado['error']}), resultado ['code']
    return jsonify(resultado['data']), resultado['code']
