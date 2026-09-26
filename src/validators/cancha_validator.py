import re

CAMPOS_PERMITIDOS = {
    "nombre",
    "id_deporte",
    "precio_hora",
    "techada",
    "activa",
}

CAMPOS_OBLIGATORIOS = {
    "nombre",
    "id_deporte",
    "precio_hora",
}

CAMPOS_PERMITIDOS_PATCH = {
    "nombre",
    "precio_hora",
    "techada",
    "activa",
}
ALLOWED_FIELDS = {"fecha", "hora_inicio", "hora_fin", "id_deporte", "techada"}

def validate_disponibilidad(data):
    if not isinstance(data, dict):
        return False, "El cuerpo debe ser uno objeto JSON."
    if not data:
        return False, "El cuerpo no puede estar vacío."

    unknown_fields = set(data.keys()) - ALLOWED_FIELDS
    if unknown_fields:
        return False, f"Campos desconocidos: {', '.join(unknown_fields)}"

    if "fecha" not in data:
        return False, "El campo fecha es obligatorio."
    
    if not isinstance(data["fecha"], str):
        return False, "El campo fecha debe ser un string con formato (YYYY-MM-DD)."
    if not data["fecha"].strip():
        return False, "El campo fecha no puede estar vacío."
    if not is_valid_date(data["fecha"]):
        return False, "El campo fecha no tiene un formato valido"

    for campo in ("hora_inicio", "hora_fin"):
        if campo not in data:
            return False, f"El campo {campo} es obligatorio."

        if not isinstance(data[campo], str):
            return False, f"El campo {campo} debe ser un string con formato (HH:MM:SS)."
        if not data[campo].strip():
            return False, f"El campo {campo} no puede estar vacío."
        if not is_valid_time(data[campo]):
            return False, f"El campo {campo} no tiene un formato válido."

    if "id_deporte" in data and not isinstance(data["id_deporte"], int):
        return False, "El campo id_deporte debe ser un número entero."

    if "techada" in data and not isinstance(data["techada"], bool):
        return False, "El campo techada debe ser True o False."
    return True, None

def is_valid_date(fecha):
    pattern=r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, fecha) is not None

def is_valid_time(hora):
    pattern=r"^\d{2}:\d{2}:\d{2}$"
    return re.match(pattern, hora) is not None

def validate_cancha_id(cancha_id):
    try:
        val = int(cancha_id)
    except (ValueError, TypeError):
        return False, "El id debe ser un entero."

    if val <= 0:
        return False, "El id debe ser mayor a 0."

    return True, None


def validate_canchas_query_params(args):
    valid_params = {
        "_limite",
        "_salto",
        "_id_deporte",
        "_nombre",
        "_techada",
        "_activa",
    }

    for param in args:
        if param not in valid_params:
            return (
                False,
                f"Parametro invalido: {param}",
                None,
                None,
                None,
            )

    limite_str = args.get("_limite")

    if limite_str is not None:
        try:
            limite = int(limite_str)
        except ValueError:
            return (
                False,
                "Parametro invalido: _limite debe ser un entero",
                None,
                None,
                None,
            )

        if limite < 1 or limite > 100:
            return (
                False,
                "Parametro invalido: _limite debe estar entre 1 y 100",
                None,
                None,
                None,
            )
    else:
        limite = 10

    salto_str = args.get("_salto")

    if salto_str is not None:
        try:
            salto = int(salto_str)
        except ValueError:
            return (
                False,
                "Parametro invalido: _salto debe ser un entero",
                None,
                None,
                None,
            )

        if salto < 0:
            return (
                False,
                "Parametro invalido: _salto debe ser mayor o igual a 0",
                None,
                None,
                None,
            )
    else:
        salto = 0

    filtros = {}

    if "_id_deporte" in args:
        try:
            dep_id = int(args.get("_id_deporte"))
        except ValueError:
            return (
                False,
                "Parametro invalido: _id_deporte debe ser un entero",
                None,
                None,
                None,
            )

        if dep_id <= 0:
            return (
                False,
                "Parametro invalido: _id_deporte debe ser mayor a 0",
                None,
                None,
                None,
            )

        filtros["id_deporte"] = dep_id

    if "_nombre" in args:
        filtros["nombre"] = args.get("_nombre")

    if "_techada" in args:
        val = args["_techada"].lower()

        if val not in ["true", "false"]:
            return (
                False,
                "Parametro invalido: _techada debe ser true o false",
                None,
                None,
                None,
            )

        filtros["techada"] = 1 if val == "true" else 0

    if "_activa" in args:
        val = args["_activa"].lower()

        if val not in ["true", "false"]:
            return (
                False,
                "Parametro invalido: _activa debe ser true o false",
                None,
                None,
                None,
            )

        filtros["activa"] = 1 if val == "true" else 0

    return True, None, limite, salto, filtros


def validate_create_cancha(data):
    if type(data) != dict:
        return False, "Los datos deben ser un diccionario."

    for campo in CAMPOS_OBLIGATORIOS:
        if campo not in data:
            return False, "Falta un campo obligatorio."

    for campo in data:
        if campo not in CAMPOS_PERMITIDOS:
            return False, "Hay un campo no permitido."

    if not isinstance(data["nombre"], str):
        return False, "El campo 'nombre' debe ser una cadena de texto."

    if data["nombre"].strip() == "":
        return False, "El campo 'nombre' no puede estar vacio."

    if type(data["id_deporte"]) != int:
        return False, "El campo 'id_deporte' debe ser un entero."

    if data["id_deporte"] <= 0:
        return False, "El campo 'id_deporte' debe ser un entero positivo."

    if type(data["precio_hora"]) != int:
        return False, "El campo 'precio_hora' debe ser un entero."

    if data["precio_hora"] <= 0:
        return False, "El campo 'precio_hora' debe ser un entero positivo."

    if "techada" in data and type(data["techada"]) != bool:
        return False, "El campo 'techada' debe ser true o false."

    if "activa" in data and type(data["activa"]) != bool:
        return False, "El campo 'activa' debe ser true o false."

    return True, None


def validate_patch_cancha(data):
    if type(data) != dict:
        return False, "Los datos deben ser un diccionario."

    if len(data) == 0:
        return False, "Los datos no pueden estar vacíos."

    for campo in data:
        if campo not in CAMPOS_PERMITIDOS_PATCH:
            return False, "Hay un campo no permitido."

    if "nombre" in data:
        if not isinstance(data["nombre"], str):
            return False, "El campo 'nombre' debe ser una cadena de texto."

        if data["nombre"].strip() == "":
            return False, "El campo 'nombre' no puede estar vacio."

    if "precio_hora" in data:
        if type(data["precio_hora"]) != int:
            return False, "El campo 'precio_hora' debe ser un entero."

        if data["precio_hora"] <= 0:
            return False, "El campo 'precio_hora' debe ser un entero positivo."

    if "techada" in data and type(data["techada"]) != bool:
        return False, "El campo 'techada' debe ser true o false."

    if "activa" in data and type(data["activa"]) != bool:
        return False, "El campo 'activa' debe ser true o false."

    return True, None