import re

ALLOWED_FIELDS = {"nombre", "email", "activo"}


def validate_update_socio(data):
    if not isinstance(data, dict):
        return False, "El cuerpo debe ser uno objeto JSON."

    if not data:
        return False, "El cuerpo no puede estar vacío."

    unknown_fields = set(data.keys()) - ALLOWED_FIELDS

    if unknown_fields:
        return False, f"Campos desconocidos: {', '.join(unknown_fields)}"

    if "nombre" in data:
        if not isinstance(data["nombre"], str):
            return False, "El nombre debe ser un string."

        if not data["nombre"].strip():
            return False, "El nombre no puede estar vacío."

    if "email" in data:
        if not isinstance(data["email"], str):
            return False, "El email tiene que ser un string."

        email = data["email"].strip()

        if not is_valid_email(email):
            return False, "El email no tiene un formato válido."

    if "activo" in data and not isinstance(data["activo"], bool):
        return False, "Activo debe ser True o False."

    return True, None


def is_valid_email(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(pattern, email) is not None


CREATE_FIELDS = {"nombre", "email"}
QUERY_PARAMS = {"nombre", "activo", "_limit", "_offset"}


def is_valid_email_create(email):
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.fullmatch(pattern, email) is not None


def validate_create_socio(data):
    if not isinstance(data, dict):
        return False, "El cuerpo debe ser un objeto JSON."

    if "nombre" not in data or "email" not in data:
        return False, "Nombre y email son obligatorios."

    unknown_fields = set(data.keys()) - CREATE_FIELDS

    if unknown_fields:
        return False, "Hay campos desconocidos."

    if not isinstance(data["nombre"], str):
        return False, "El nombre debe ser un string."

    if not data["nombre"].strip():
        return False, "El nombre no puede estar vacio."

    if not isinstance(data["email"], str):
        return False, "El email debe ser un string."

    email = data["email"].strip()

    if not is_valid_email_create(email):
        return False, "El email no tiene un formato valido."

    return True, None


def validate_socios_query_params(args):
    for param in args:
        if param not in QUERY_PARAMS:
            return False, f"Parametro desconocido: {param}", None, None, None
    try:
        limit = int(args.get("_limit", 10))
    except (ValueError, TypeError):
        return False, "_limit debe ser un entero.", None, None, None

    if limit < 1 or limit > 100:
        return False, "_limit debe estar entre 1 y 100.", None, None, None

    try:
        offset = int(args.get("_offset", 0))
    except (ValueError, TypeError):
        return False, "_offset debe ser un entero.", None, None, None

    if offset < 0:
        return False, "_offset debe ser mayor o igual a 0.", None, None, None

    filtros = {}

    if "nombre" in args:
        filtros["nombre"] = args.get("nombre").strip()

    if "activo" in args:
        activo = args.get("activo")

        if activo not in ("true", "false"):
            return False, "activo debe ser true o false.", None, None, None

        filtros["activo"] = activo == "true"

    return True, None, filtros, limit, offset
