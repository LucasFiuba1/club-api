from repositories.socios.socio_repository import (
    get_socio_by_email,
    get_socio_by_id,
    update_socio,
)
from utils.error_utils import build_error, socio_not_found_error
from validators.socio_validator import validate_update_socio


def get_socio(socio_id):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return None, socio_not_found_error(socio_id), 404

    return socio, None, 200


def update_socio_service(socio_id, data):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return None, socio_not_found_error(socio_id), 404

    valid, error = validate_update_socio(data)

    if not valid:
        return (
            None,
            build_error(
                "ERRO_VALIDACION",
                "El cuerpo de la solicitud es invalido.",
                error,
            ),
            400,
        )

    if "nombre" in data:
        data["nombre"] = data["nombre"].strip()

    if "email" in data:
        data["email"] = data["email"].strip().lower()

        socio_with_email = get_socio_by_email(data["email"])

        if socio_with_email is not None and socio_with_email["id"] != socio_id:
            return (
                None,
                build_error(
                    "EMAIL_YA_REGISTRADO",
                    "Email ya registrado.",
                    "El email ya pertenece a otro socio",
                ),
                409,
            )

    update_socio(socio_id, data)

    return None, 204
