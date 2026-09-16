from validators.cancha_validator import validate_create_cancha, validate_patch_cancha
from repositories.canchas.cancha_repository import get_deporte_by_id, create_cancha, get_cancha_by_id


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
    valid, error = validate_patch_cancha(data)

    if valid == False:
        return None, error, 400

    if "nombre" in data:
        nombre = data["nombre"].strip()
        data["nombre"] = nombre

    cancha = get_cancha_by_id(id_cancha)

    if cancha is None:
        return None, "La cancha no existe", 404

    
    


    