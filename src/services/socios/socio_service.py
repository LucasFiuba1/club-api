from repositories.socios.socio_repository import get_socio_by_email, get_socio_by_id
from validators.socio_validator import validate_update_socio


def get_socio(socio_id):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return None, {"error": "Socio no encontrado."}, 404

    return socio, None, 200


def update_socio_service(socio_id, data):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return None, {"error": "Socio no encontrado."}, 404

    valid, error = validate_update_socio(socio_id)

    if not valid:
        return False, {"error": error}, 400

    if "nombre" in data:
        data["nombre"] = data["nombre"].strip()

    if "email" in data:
        data["email"] = data["email"].strip().lower()

        socio_with_email = get_socio_by_email(data["email"])

        if socio_with_email is not None and socio_with_email["id"] != socio_id:
            return None, {{"error": "El email ya esta registrado."}}, 409

    updated_socio = (socio_id,data)

    return updated_socio, None, 200