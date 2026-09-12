import re

ALLOWED_FIELDS = {
    "nombre",
    "email",
    "activo"
}

def validate_update_socio(socio_id, data):
    if not isinstance(data, dict):
        return False, "El cuerpo debe ser uno objeto JSON."

    if not data:
        return False, "El cuerpo no puede estar vacío."

    unknown_fields = set(data.keys()) - ALLOWED_FIELDS

    if unknown_fields:
        return False, {
            f"Campos desconocidos: {", ".join(unknown_fields)}"
        }, 400

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
    