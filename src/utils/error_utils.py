def build_error(code, message, description):
    return {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": "error",
                "description": description,
            }
        ]
    }


def socio_not_found_error(socio_id):
    return build_error(
        "SOCIO_NO_ENCONTRADO",
        "Socio no encontrado.",
        f"No existe un socio con id: {socio_id}",
    )
