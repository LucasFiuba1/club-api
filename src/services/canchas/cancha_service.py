from datetime import datetime, time, timedelta, timezone

from repositories.canchas.cancha_repository import (
    get_canchas_disponibles,
)
from utils.error_utils import (
    invalid_reservation_duration_error,
    time_out_of_range_error,
    time_not_top_of_hour_error,
)

GMT3 = timezone(timedelta(hours=-3))

def get_canchas_disponibles_service(fecha, hora_inicio, hora_fin, id_deporte=None, techada=None):
    
    hora_inicio_obj=datetime.strptime(hora_inicio, "%H:%M:%S").replace(tzinfo=GMT3)
    hora_fin_obj=datetime.strptime(hora_fin, "%H:%M:%S").replace(tzinfo=GMT3)
    duracion_reserva=hora_fin_obj-hora_inicio_obj

    if hora_inicio_obj.minute != 0 or hora_inicio_obj.second != 0:
        return None, time_not_top_of_hour_error(hora_inicio), 400
    if hora_fin_obj.minute != 0 or hora_fin_obj.second != 0:
        return None, time_not_top_of_hour_error(hora_fin), 400
    
    if hora_inicio_obj.time() < time(8, 0, 0) or hora_inicio_obj.time() > time(23, 0, 0):
        return None, time_out_of_range_error(hora_inicio), 400
    if hora_fin_obj.time() < time(8, 0, 0) or hora_fin_obj.time() > time(23, 0, 0):
        return None, time_out_of_range_error(hora_fin), 400
    
    duracion_horas=duracion_reserva.total_seconds()/3600
    if duracion_horas<1 or duracion_horas>3:
        return None, invalid_reservation_duration_error(duracion_horas), 400
    
    canchas=get_canchas_disponibles(fecha, hora_inicio, hora_fin, id_deporte, techada)
    return canchas, None, 200