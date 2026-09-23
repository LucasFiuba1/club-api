from datetime import datetime, time, timedelta, timezone
from urllib.parse import urlencode

from src.repositories.canchas.cancha_repository import (
    create_cancha,
    delete_cancha,
    get_all_deportes,
    get_cancha_by_id,
    get_canchas,
    get_canchas_disponibles,
    get_deporte_by_id,
    get_reserva_by_cancha,
    update_cancha,
)
from src.utils.error_utils import (
    build_error,
    invalid_reservation_duration_error,
    time_not_top_of_hour_error,
    time_out_of_range_error,
)
from src.validators.cancha_validator import (
    validate_cancha_id,
    validate_canchas_query_params,
    validate_create_cancha,
    validate_patch_cancha,
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



def get_deportes_service():
    deportes = get_all_deportes()
    return deportes, None, 200


def get_cancha_service(cancha_id):
    valid, error = validate_cancha_id(cancha_id)

    if not valid:
        return (
            None,
            build_error(
                "ERROR_VALIDACION",
                "El id de la cancha es invalido.",
                error,
            ),
            400,
        )

    cancha = get_cancha_by_id(cancha_id)

    if cancha is None:
        return (
            None,
            build_error(
                "CANCHA_NO_ENCONTRADA",
                "La cancha no fue encontrada.",
                f"No se encontro la cancha con id {cancha_id}",
            ),
            404,
        )

    return cancha, None, 200


def get_canchas_service(base_url, args):
    valid, error, limite, salto, filtros = validate_canchas_query_params(args)

    if not valid:
        return (
            None,
            build_error(
                "ERROR_VALIDACION",
                "Los parametros de la consulta son invalidos.",
                error,
            ),
            400,
        )

    items, total = get_canchas(filtros, limite, salto)

    filtros_params = {}

    if "id_deporte" in filtros:
        filtros_params["id_deporte"] = filtros["id_deporte"]

    if "nombre" in filtros:
        filtros_params["nombre"] = filtros["nombre"]

    if "techada" in filtros:
        filtros_params["techada"] = "true" if filtros["techada"] == 1 else "false"

    if "activa" in filtros:
        filtros_params["activa"] = "true" if filtros["activa"] == 1 else "false"

    def build_link(salto_pagina):
        parametros = dict(filtros_params)
        parametros["_limite"] = limite
        parametros["_salto"] = salto_pagina

        return f"{base_url}?{urlencode(parametros)}"

    first_link = build_link(0)

    prev_link = build_link(max(0, salto - limite)) if salto > 0 else None

    next_link = build_link(salto + limite) if salto + limite < total else None

    last_salto = ((total - 1) // limite) * limite if total > 0 else 0

    last_link = build_link(last_salto)

    response_data = {
        "canchas": items,
        "_links": {
            "_first": first_link,
            "_prev": prev_link,
            "_next": next_link,
            "_last": last_link,
        },
    }

    return response_data, None, 200


def create_cancha_service(data):
    valid, error = validate_create_cancha(data)

    if not valid:
        return (
            None,
            build_error(
                "ERROR_VALIDACION",
                "El cuerpo de la solicitud es invalido.",
                error,
            ),
            400,
        )

    techada = data.get("techada", False)
    activa = data.get("activa", True)
    nombre = data["nombre"].strip()

    data["nombre"] = nombre
    data["techada"] = techada
    data["activa"] = activa

    deporte = get_deporte_by_id(data["id_deporte"])

    if deporte is None:
        return (
            None,
            build_error(
                "DEPORTE_NO_ENCONTRADO",
                "Deporte no encontrado",
                f"No existe un deporte con id: {data['id_deporte']}",
            ),
            404,
        )

    create_cancha(data)

    return None, None, 201


def patch_cancha_service(id_cancha, data):
    cancha = get_cancha_by_id(id_cancha)

    if cancha is None:
        return (
            build_error(
                "CANCHA_NO_ENCONTRADA",
                "Cancha no encontrada",
                f"No existe una cancha con id: {id_cancha}",
            ),
            404,
        )

    valid, error = validate_patch_cancha(data)

    if not valid:
        return (
            build_error(
                "ERROR_VALIDACION",
                "El cuerpo de la solicitud es invalido",
                error,
            ),
            400,
        )

    if "nombre" in data:
        data["nombre"] = data["nombre"].strip()

    update_cancha(id_cancha, data)

    return None, 204


def delete_cancha_service(id_cancha):
    cancha = get_cancha_by_id(id_cancha)

    if cancha is None:
        return (
            build_error(
                "CANCHA_NO_ENCONTRADA",
                "Cancha no encontrada",
                f"No existe una cancha con id: {id_cancha}",
            ),
            404,
        )

    reserva = get_reserva_by_cancha(id_cancha)

    if reserva is not None:
        return (
            build_error(
                "CANCHA_CON_RESERVAS",
                "La cancha tiene reservas asociadas",
                f"No se puede eliminar la cancha con id: {id_cancha} porque tiene reservas asociadas",
            ),
            409,
        )

    delete_cancha(id_cancha)

    return None, 204

