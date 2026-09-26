from urllib.parse import urlencode

from mysql.connector import IntegrityError

from src.repositories.socios.socio_repository import (
    create_socio,
    get_socio_by_email,
    get_socio_by_id,
    get_socios,
    update_socio,
)
from src.utils.error_utils import build_error, socio_not_found_error
from src.validators.socio_validator import (
    validate_create_socio,
    validate_socios_query_params,
    validate_update_socio,
)


def get_socio(socio_id):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return None, socio_not_found_error(socio_id), 404

    return socio, None, 200


def update_socio_service(socio_id, data):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return socio_not_found_error(socio_id), 404

    valid, error = validate_update_socio(data)

    if not valid:
        return (
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
                build_error(
                    "EMAIL_YA_REGISTRADO",
                    "Email ya registrado.",
                    "El email ya pertenece a otro socio",
                ),
                409,
            )

    update_socio(socio_id, data)

    return None, 204

def create_socio_service(data):
    valid, error = validate_create_socio(data)

    if not valid:
        return build_error(
            "ERROR_VALIDACION",
            "Datos invalidos.",
            error
        ), 400

    socio = {
        "nombre": data["nombre"].strip(),
        "email": data["email"].strip().lower(),
        "activo": True
    }

    try:
        create_socio(socio)

    except IntegrityError as error_db:
        if error_db.errno == 1062:
            return build_error(
                "EMAIL_YA_REGISTRADO",
                "Email ya registrado.",
                "Ya existe un socio con ese email."
            ), 409

        raise

    return None, 201


def get_socios_service(base_url, args):
    valid, error, filtros, limit, offset = validate_socios_query_params(args)

    if not valid:
        return None, build_error(
            "ERROR_VALIDACION",
            "Parametros invalidos.",
            error
        ), 400

    socios, total = get_socios(filtros, limit, offset)

    def crear_link(nuevo_offset):
        parameters = dict(args)

        parameters["_limit"] = limit
        parameters["_offset"] = nuevo_offset

        return {
            "href": base_url + "?" + urlencode(parameters)
            }

    first = crear_link(0)

    prev = None
    if offset > 0:
        prev = crear_link(max(0, offset - limit))

    next_link = None
    if offset + limit < total:
        next_link = crear_link(offset + limit)

    if total == 0:
        last_offset = 0
    else:
        last_offset = ((total - 1) // limit) * limit

    last = crear_link(last_offset)

    respuesta = {
        "socios": socios,
        "_links": {
            "_first": first,
            "_prev": prev,
            "_next": next_link,
            "_last": last
        }
    }

    return respuesta, None, 200
