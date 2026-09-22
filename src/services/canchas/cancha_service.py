from urllib import urlencode

from repositories.canchas.cancha_repository import (
    get_all_deportes,
    get_canchas_by_id,
    get_canchas,

)

from utils.error_utils import build_error
from validators.cancha_validator import (
    validate_canchas_query_params,
    validate_cancha_id
)

def get_deportes_service():
    deportes = get_all_deportes()
    return deportes, None, 200

def get_cancha_service(cancha_id):
    valid, error = validate_cancha_id(cancha_id)

    if not valid:
        return(
            None, 
            build_error(
                "ERRO_VALIDACION",
                "El id de la cancha es invalido.",
                error,
            ),
            400
        )
    cancha = get_canchas_by_id(cancha_id)
    if cancha is None:
        return (
            None,
            build_error(
                "CANCHA_NO_ENCONTRADA",
                "La cancha no fue encontrada.",
                f"No se encontro la cancha con id {cancha_id}",
            ),
            404
        )
    return cancha, None, 200


def get_canchas_service(base_url, args):
    valid, error, limite, salto, filtros = validate_canchas_query_params(args)

    if not valid:
        return (
            None,
            build_error(
                "ERRO_VALIDACION",
                "Los parametros de la consulta son invalidos.",
                error,
            ),
            400,
        )

    items, total = get_canchas(filtros, limite, salto)

    filtros_params = {}

    if "id_deporte" in filtros:
        filtros_params["id_deporte"] = filtros["id_deporte"]
    if "nombre" in filtros:
        filtros_params["nombre"] = filtros["nombre"]
    if "techada" in filtros:
            filtros_params["techada"] = "true" if  filtros["techada"] == 1 else "false"
    if "activa" in filtros:
               filtros_params["activa"] = "true" if  filtros["activa"] == 1 else "false"


    def build_link(salto_pagina):
        parametros = dict(filtros_params)
        parametros["_limite"] = limite
        parametros["_salto"] = salto_pagina
        return f"{base_url}?{urlencode(parametros)}"

    first_link = build_link(0)
    prev_link = build_link(max(0, salto - limite)) if salto > 0 else None
    next_link = build_link(salto + limite) if salto + limite < total else None
    last_salto = ((total - 1) // limite ) * limite if total > 0 else 0
    last_link = build_link(last_salto)

    response_data = {
         "canchas": items,
         "_links":{
              "_first": first_link,
              "_prev": prev_link,
              "_next": next_link,
              "_last": last_link
         },
    }

    return response_data, None, 200