from datetime import datetime, time, timedelta, timezone

from repositories.canchas.cancha_repository import get_cancha_by_id
from repositories.reservas.reserva_repository import (
    create_reserva,
    existe_superposicion,
)
from repositories.socios.socio_repository import get_socio_by_id
from src.repositories.reservas.reserva_repository import (
    get_reserva_by_id,
    get_reservas_db,
    update_estado_db,
)
from utils.error_utils import (
    cancha_inactive_error,
    cancha_not_found_error,
    cancha_overlap_error,
    invalid_reservation_duration_error,
    reserva_not_future_error,
    socio_inactive_error,
    socio_not_found_error,
    time_not_top_of_hour_error,
    time_out_of_range_error,
)

GMT3 = timezone(timedelta(hours=-3))


def _formatear_reserva(reserva):
    if not reserva:
        return None
    for campo in ["fecha_hora_inicio", "fecha_hora_fin"]:
        if isinstance(reserva[campo], datetime):
            reserva[campo] = reserva[campo].strftime("%Y-%m-%dT%H:%M:%S.000000-03:00")
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

    estados_validos = ["confirmada", "cancelada", "finalizada"]
    if nuevo_estado not in estados_validos:
        return {"error": "Estado desconocido", "code": 400}

    reserva = get_reserva_by_id(reserva_id)
    if not reserva:
        return {"error": "Reserva no encontrada", "code": 404}

    estado_actual = reserva["estado"]

    if nuevo_estado == estado_actual:
        return {"data": _formatear_reserva(reserva), "code": 200}

    if estado_actual in ["cancelada", "finalizada"]:
        return {"error": f"La reserva ya esta {estado_actual}", "code": 409}

    ahora = datetime.now()  # noqa: DTZ005
    inicio = reserva["fecha_hora_inicio"]
    fin = reserva["fecha_hora_fin"]

    if nuevo_estado == "cancelada" and ahora >= inicio:
        return {"error": "No se puede cancelar una reserva que ya comenzo", "code": 409}

    if nuevo_estado == "finalizada" and ahora < fin:
        return {
            "error": "No se puede finalizar una reserva que no ha terminado",
            "code": 409,
        }

    update_estado_db(reserva_id, nuevo_estado)
    reserva_actualizada = get_reserva_by_id(reserva_id)
    return {"data": _formatear_reserva(reserva_actualizada), "code": 200}


def create_reserva_service(id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin):
    fecha_hora_inicio_obj = datetime.strptime(
        fecha_hora_inicio, "%Y-%m-%dT%H:%M:%S.%f%z"
    ).replace(tzinfo=GMT3)
    fecha_hora_fin_obj = datetime.strptime(
        fecha_hora_fin, "%Y-%m-%dT%H:%M:%S.%f%z"
    ).replace(tzinfo=GMT3)
    fecha = fecha_hora_inicio_obj.strftime("%Y-%m-%d")
    hora_inicio = fecha_hora_inicio_obj.strftime("%H:%M:%S")
    hora_fin = fecha_hora_fin_obj.strftime("%H:%M:%S")
    if fecha_hora_inicio_obj.minute != 0 or fecha_hora_inicio_obj.second != 0:
        return None, time_not_top_of_hour_error(fecha_hora_inicio), 400
    if fecha_hora_fin_obj.minute != 0 or fecha_hora_fin_obj.second != 0:
        return None, time_not_top_of_hour_error(fecha_hora_fin), 400

    if fecha_hora_inicio_obj.time() < time(
        8, 0, 0
    ) or fecha_hora_inicio_obj.time() > time(23, 0, 0):
        return None, time_out_of_range_error(fecha_hora_inicio), 400
    if fecha_hora_fin_obj.time() < time(8, 0, 0) or fecha_hora_fin_obj.time() > time(
        23, 0, 0
    ):
        return None, time_out_of_range_error(fecha_hora_fin), 400

    duracion_reserva = fecha_hora_fin_obj - fecha_hora_inicio_obj
    duracion_horas = duracion_reserva.total_seconds() / 3600
    if duracion_horas < 1 or duracion_horas > 3:
        return None, invalid_reservation_duration_error(duracion_horas), 400

    if fecha_hora_inicio_obj <= datetime.now(GMT3):
        return None, reserva_not_future_error(fecha_hora_inicio), 400

    socio = get_socio_by_id(id_socio)
    if socio is None:
        return None, socio_not_found_error(id_socio), 404
    if not socio["activo"]:
        return None, socio_inactive_error(id_socio), 400

    cancha = get_cancha_by_id(id_cancha)
    if cancha is None:
        return None, cancha_not_found_error(id_cancha), 404
    if not cancha["activa"]:
        return None, cancha_inactive_error(id_cancha), 400
    if existe_superposicion(id_cancha, fecha, hora_inicio, hora_fin):
        return None, cancha_overlap_error(id_cancha, fecha, hora_inicio, hora_fin), 409

    precio_hora = cancha["precio_hora"]
    precio_total = precio_hora * duracion_horas
    reserva_id = create_reserva(
        id_socio,
        id_cancha,
        fecha_hora_inicio,
        fecha_hora_fin,
        "confirmada",
        precio_hora,
        precio_total,
    )
    reserva_creada = {
        "id": reserva_id,
        "id_socio": id_socio,
        "id_cancha": id_cancha,
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
        "estado": "confirmada",
        "precio_hora": precio_hora,
        "precio_total": precio_total,
    }
    return reserva_creada, None, 201
