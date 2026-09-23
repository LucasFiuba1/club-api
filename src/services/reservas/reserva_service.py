from datetime import datetime, time, timedelta, timezone

from repositories.canchas.cancha_repository import get_cancha_by_id
from repositories.reservas.reserva_repository import (
    create_reserva,
    existe_superposicion,
)
from repositories.socios.socio_repository import get_socio_by_id
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

GMT3 =  timezone(timedelta(hours=-3))
def create_reserva_service(id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin):
    fecha_hora_inicio_obj=datetime.strptime(fecha_hora_inicio, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=GMT3)
    fecha_hora_fin_obj=datetime.strptime(fecha_hora_fin, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=GMT3)
    fecha=fecha_hora_inicio_obj.strftime("%Y-%m-%d")
    hora_inicio=fecha_hora_inicio_obj.strftime("%H:%M:%S")
    hora_fin=fecha_hora_fin_obj.strftime("%H:%M:%S")
    if fecha_hora_inicio_obj.minute != 0 or fecha_hora_inicio_obj.second != 0:
        return None, time_not_top_of_hour_error(fecha_hora_inicio), 400
    if fecha_hora_fin_obj.minute != 0 or fecha_hora_fin_obj.second != 0:
        return None, time_not_top_of_hour_error(fecha_hora_fin), 400

    if fecha_hora_inicio_obj.time() < time(8, 0, 0) or fecha_hora_inicio_obj.time() > time(23, 0, 0):
        return None, time_out_of_range_error(fecha_hora_inicio), 400
    if fecha_hora_fin_obj.time() < time(8, 0, 0) or fecha_hora_fin_obj.time() > time(23, 0, 0):
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
    
    precio_hora=cancha["precio_hora"]
    precio_total=precio_hora*duracion_horas
    reserva_id=create_reserva(id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, 'confirmada', precio_hora, precio_total)
    reserva_creada={
        "id":reserva_id,
        "id_socio":id_socio,
        "id_cancha":id_cancha,
        "fecha_hora_inicio": fecha_hora_inicio,
        "fecha_hora_fin": fecha_hora_fin,
        "estado": "confirmada",
        "precio_hora":precio_hora,
        "precio_total": precio_total,
    }
    return reserva_creada, None, 201
