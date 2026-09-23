import re

ALLOWED_FIELDS = {"id_socio", "id_cancha", "fecha_hora_inicio", "fecha_hora_fin"}

def validate_reserva(data):
    if not isinstance(data, dict):
        return False, "El cuerpo debe ser uno objeto JSON."
    if not data:
        return False, "El cuerpo no puede estar vacío."
    
    unknown_fields = set(data.keys()) - ALLOWED_FIELDS
    if unknown_fields:
        return False, f"Campos desconocidos: {', '.join(unknown_fields)}"

    for campo in ("id_socio", "id_cancha"):
        if campo not in data:
            return False, f"El campo {campo} es obligatorio."

        if not isinstance(data[campo], int):
            return False, f"El campo {campo} debe ser un número entero."
        
    for campo in ("fecha_hora_inicio", "fecha_hora_fin"):
        if campo not in data:
            return False, f"El campo {campo} es obligatorio."

        if not isinstance(data[campo], str):
            return False, f"El campo {campo} debe ser un string con formato (YYYY-MM-DDTHH:MM:SS.ffffff-03:00)."
        if not data[campo].strip():
            return False, f"El campo {campo} no puede estar vacío."
        if not is_valid_datetime(data[campo]):
            return False, f"El campo {campo} no tiene un formato válido."
    return True, None

def is_valid_datetime(fecha_hora):
    pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}-\d{2}:\d{2}$"
    return re.match(pattern, fecha_hora) is not None