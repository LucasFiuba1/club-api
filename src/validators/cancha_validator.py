import re

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

    if "id_deporte" in data:
        if not isinstance(data["id_deporte"], int):
            return False, "El campo id_deporte debe ser un número entero."

    if "techada" in data:
        if not isinstance(data["techada"], bool):
            return False, "El campo techada debe ser True o False."
    return True, None

def is_valid_date(fecha):
    pattern=r"^\d{4}-\d{2}-\d{2}$"
    return re.match(pattern, fecha) is not None

def is_valid_time(hora):
    pattern=r"^\d{2}:\d{2}:\d{2}$"
    return re.match(pattern, hora) is not None