from repositories.socios.socio_repository import get_socio_by_id


def get_socio(socio_id):
    socio = get_socio_by_id(socio_id)

    if socio is None:
        return None, {
            "error": "Socio no encontrado."
        }, 404
    
    return socio, None, 200