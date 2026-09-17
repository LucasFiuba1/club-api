from validators.cancha_validator import validate_create_cancha, validate_patch_cancha
from repositories.canchas.cancha_repository import get_deporte_by_id, create_cancha, get_cancha_by_id, update_cancha, get_reserva_by_cancha, delete_cancha


def create_cancha_service(data):
    valid, error = validate_create_cancha(data)

    if valid == False:
        return None, error, 400

    techada = data.get("techada", False)
    activa = data.get("activa", True)
    nombre = data["nombre"].strip()

    data ["nombre"] = nombre
    data ["techada"] = techada
    data ["activa"] = activa

    deporte = get_deporte_by_id(data["id_deporte"])
    
    if deporte is None:
        return None, "El deporte no existe", 404
    
    create_cancha(data)
    return None, None, 201


def patch_cancha_service(id_cancha, data):
    cancha = get_cancha_by_id(id_cancha)

    if cancha is None:
        return "La cancha no existe", 404

    valid, error = validate_patch_cancha(data)

    if valid == False:
        return error, 400

    if "nombre" in data:
        nombre = data["nombre"].strip()
        data["nombre"] = nombre

    update_cancha(id_cancha, data)

    return None, 204

def delete_cancha_service(id_cancha):
    cancha = get_cancha_by_id(id_cancha)

    if cancha is None:
        return "La cancha no existe", 404

    reserva = get_reserva_by_cancha(id_cancha)

    if reserva is not None:
        return "La cancha tiene reservas asociadas", 409

    delete_cancha(id_cancha)
    return None, 204

    