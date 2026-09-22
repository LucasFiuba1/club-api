from flask import Blueprint, jsonify, request

from services.reservas.reservas_service import (
    cambiar_estado_reserva,
    listar_reservas,
    obtener_reserva,
)

reserva_bp = Blueprint('reserva_bp', __name__)

@reserva_bp.route('/reservas', methods=['GET'])
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


@reserva_bp.route('/reservas/<int:reserva_id>', methods=['GET'])
def get_reserva_by_id(reserva_id):
    reserva = obtener_reserva(reserva_id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404

    return jsonify(reserva), 200

@reserva_bp.route('/reservas/<int:reserva_id>/estado', methods=['PUT'])
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
