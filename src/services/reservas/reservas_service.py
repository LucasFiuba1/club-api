from datetime import datetime

from repositories.reservas.reservas_repository import (
    get_reserva_by_id,
    get_reservas_db,
    update_estado_db,
)


def _formatear_reserva(reserva):
    if not reserva:
        return None
    for campo in ['fecha_hora_inicio', 'fecha_hora_fin']:
        if isinstance(reserva[campo], datetime):
            reserva[campo] = reserva[campo].strftime('%Y-%m-%dT%H:%M:%S.000000-03:00')
    return reserva

def listar_reservas(filters, limit, offset):
    reservas, total = get_reservas_db(filters, limit, offset)
    return [_formatear_reserva(r) for r in reservas], total


def obtener_reserva(reserva_id):
    """
    Busca una reservapor su ID.
    Devuelve eldiccionario con los datos o None si no existe.
    """
    reserva = get_reserva_by_id(reserva_id)
    return _formatear_reserva(reserva)

def cambiar_estado_reserva(reserva_id, nuevo_estado):

    estados_validos = ['confirmada', 'cancelada', 'finalizada']
    if nuevo_estado not in estados_validos:
        return {"error": "Estado desconocido", "code": 400}
    
    reserva = get_reserva_by_id(reserva_id)
    if not reserva:
        return {"error": "Reserva no encontrada", "code": 404}

    estado_actual = reserva['estado']

    if nuevo_estado == estado_actual:
        return {"data": _formatear_reserva(reserva), "code": 200}

    if estado_actual in ['cancelada', 'finalizada']:
        return {"error": f"La reserva ya esta {estado_actual}", "code": 409}

    ahora = datetime.now() # noqa: DTZ005
    inicio = reserva['fecha_hora_inicio']
    fin = reserva['fecha_hora_fin']

    if nuevo_estado == 'cancelada' and ahora >= inicio:
        return {"error": "No se puede cancelar una reserva que ya comenzo", "code": 409}

    if nuevo_estado == 'finalizada' and ahora < fin:
        return {"error": "No se puede finalizar una reserva que no ha terminado", "code": 409}

    
    update_estado_db(reserva_id, nuevo_estado)
    reserva_actualizada = get_reserva_by_id(reserva_id)
    return {"data": _formatear_reserva(reserva_actualizada), "code": 200}