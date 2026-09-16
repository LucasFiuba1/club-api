def vlaidate_cancha_id(cancha_id):
    try:
        val = int(cancha_id)
    except (ValueError, TypeError):
        return False, None
    if val <= 0:
        return False, 
    return True, None

def validate_canchas_query_params(args):

    valid_params = {"_limite", "_salto", "_id_deporte", "_nombre", "_techada", "_activa"}

    for param in args.keys():
        if param not in valid_params:
            return False, f"Parametro invalido: {param}"

    limite_str = args.get("_limite")
    if limite_str is not None:
        try:
            limite = int(limite_str)
        except ValueError:
            return False, "Parametro invalido: _limite debe ser un entero", None, None, None
        if limite < 1 or limite > 100:
            return False, "Parametro invalido: _limite debe estar entre 1 y 100", None, None, None
    else:
        limite = 10


    salto_str = args.get("_salto")
    if salto_str is not None:
        try:
            salto = int(salto_str)
        except ValueError:
            return False, "Parametro invalido: _salto debe ser un entero", None, None, None
        if salto < 0:
            return False, "Parametro invalido: _salto debe ser mayor o igual a 0", None, None, None
    else:
        salto = 0


    filtros = {}

    if "id_deporte" in args:
        try:
            dep_id = int(args.get("id_deporte"))
        except ValueError:
            return False, "Parametro invalido: _id_deporte debe ser un entero", None, None, None
        if dep_id <= 0:
            return False, "Parametro invalido: _id_deporte debe ser mayor a 0", None, None, None
        filtros["id_deporte"] = dep_id

    if "_nombre" in args:
        filtros["nombre"] = args.get("_nombre")

    if "_techada" in args:
        val = args["_techada"].lower()
        if val not in ["true", "false"]:
            return False, "Parametro invalido: _techada debe ser true o false", None, None, None
        filtros["techada"] = 1 if val == "true" else 0

    if "_activa" in args:
        val = args["_activa"].lower()
        if val not in ["true", "false"]:
            return False, "Parametro invalido: _activa debe ser true o false", None, None, None
        filtros["activa"] = 1 if val == "true" else 0
    return True, None, filtros, limite, salto
