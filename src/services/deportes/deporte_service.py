from src.repositories.deportes.deporte_repository import (
    get_all_deportes,
    get_deporte_by_id,
)
from src.utils.error_utils import build_error
from src.validators.deporte_validator import validate_deporte_id


def get_deportes_service():
    deportes = get_all_deportes()
    return deportes, None, 200

def get_deporte_service(id_deporte):
    valid, error_msg = validate_deporte_id(id_deporte)
    if not valid:
        return(
            None,
            build_error("ERROR DE VALIDACION,", "PARAMETRO DE RUTA INVALIDO", error_msg),
            400,
        )
    deporte = get_deporte_by_id(int(id_deporte))
    if deporte is None:
        return(
            None,
            build_error(
                "RECURSO_NO_ENCONTRADO",
                "Deporte no encontrado.",
                f"No existe ningun deporte con id {id_deporte}",
            ),
            404,

        )
    return deporte, None, 200

