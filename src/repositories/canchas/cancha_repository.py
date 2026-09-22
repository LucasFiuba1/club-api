from db.connection import get_connection

def get_all_deportes():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT id, nombre
                FROM deportes
                ORDER BY nombre ASC
            """

            cursor.execute(query)

            return cursor.fetchall()

    finally:
        connection.close()


def get_canchas_by_id(cancha_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT id, nombre, id_deporte, precio_hora, techada, activa
                FROM canchas
                WHERE id = %s
            """

            cursor.execute(query, (cancha_id,))

            return cursor.fetchone()
    finally:
        connection.close()        

def get_canchas(filtros, limite, salto):
    conection = get_connection()

    try:
        condiciones = []
        parametros = []

        # filtro para el id deporte
        if filtros.get("id_deporte") is not None:
            condiciones.append("id_deporte = %s")
            parametros.append(filtros["id_deporte"])

        # filtro para el nombre
        if filtros.get("nombre") is not None:
            condiciones.append("LOWER (nombre) ILIKE %s")
            parametros.append(f"%{filtros['nombre'].lower()}%")

        # filtro para la techada
        if filtros.get("techada") is not None:
            condiciones.append("techada = %s")
            parametros.append(filtros["techada"])

        # filtro para activa
        if filtros.get("activa") is not None:
            condiciones.append("activa = %s")
            parametros.append(filtros["activa"])

        clausula_where = ""

        if condiciones:
            clausula_where = "WHERE " + " AND ".join(condiciones)

        with conection.cursor() as cursor:
            count_query = f"SELECT COUNT(*) FROM canchas {clausula_where}"
            cursor.execute(count_query, (parametros))
            count_result = cursor.fetchone()

            total = count_result["total"] if isinstance(count_result, dict) and "total" in count_result else count_result[0]


        query = f"""
            SELECT id, nombre, id_deporte, precio_hora, techada, activa
            FROM canchas
            {clausula_where}
            ORDER BY nombre ASC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, parametros + [limite, salto])

        items = cursor.fetchall()

        return items, total

    finally:
        conection.close()

