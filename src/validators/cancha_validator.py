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

            if data ["nombre"].strip() == "":
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