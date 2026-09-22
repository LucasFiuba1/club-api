from repositories.canchas.cancha_repository import (
    create_cancha,
    delete_cancha,
    get_cancha_by_id,
    get_deporte_by_id,
    get_reserva_by_cancha,
    update_cancha,
)
from utils.error_utils import build_error
from validators.cancha_validator import validate_create_cancha, validate_patch_cancha



def create_cancha_service(data):
    valid, error = validate_create_cancha(data)

    if valid == False:
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

    data ["nombre"] = nombre
    data ["techada"] = techada
    data ["activa"] = activa

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
                "cancha no encontrada",
                f"No existe una cancha con id: {id_cancha}",
            ),
            404,
        )

    valid, error = validate_patch_cancha(data)

    if valid == False:
        return (
            build_error(
                "ERROR_VALIDACION",
                "El cuerpo de la solicitud es invalido",
                error,
            ),
            400,
        )

    if "nombre" in data:
        nombre = data["nombre"].strip()
        data["nombre"] = nombre

    update_cancha(id_cancha, data)

    return None, 204

def delete_cancha_service(id_cancha):
    cancha = get_cancha_by_id(id_cancha)

    if cancha is None:
        return (
            build_error(
                "CANCHA_NO_ENCONTRADA",
                "cancha no encontrada",
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
                f"No se puede eliminar la concha con id: {id_cancha} porque tiene reservas asociadas",
            ),
            409,
        )

    delete_cancha(id_cancha)
    return None, 204
