from src.db.connection import get_connection

def get_canchas_disponibles(fecha, hora_inicio, hora_fin, id_deporte=None, techada=None):
    connection=get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:
            query="""
                SELECT id, nombre, id_deporte, precio_hora, techada, activa
                FROM canchas
                WHERE activa = TRUE
                    AND NOT EXISTS(
                        SELECT 1
                        FROM reservas
                        WHERE reservas.id_cancha = canchas.id
                            AND reservas.estado = 'confirmada'
                            AND reservas.fecha_hora_inicio < CONCAT(%s, ' ', %s)
                            AND reservas.fecha_hora_fin > CONCAT(%s, ' ', %s)
                    )
            """
            params = [fecha, hora_fin, fecha, hora_inicio]
            if id_deporte is not None:
                query+= " AND id_deporte = %s"
                params.append(id_deporte)

            if techada is not None:
                query+= " AND techada = %s"
                params.append(techada)
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
    finally:
        connection.close()

def create_cancha(data):
    connection = get_connection()

    try:
        keys = []
        values = []

        for key, value in data.items():
            keys.append(key)
            values.append(value)

        columns = ", ".join(keys)
        placeholders = ", ".join(["%s"] * len(values))

        with connection.cursor() as cursor:
            query = f"""
                INSERT INTO canchas ({columns})
                VALUES ({placeholders})
            """

            cursor.execute(query, values)
            cancha_id = cursor.lastrowid

        connection.commit()
        return cancha_id

    finally:
        connection.close()


def get_cancha_by_id(id_cancha):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, nombre, id_deporte, precio_hora, techada, activa
                FROM canchas
                WHERE id = %s
            """

            cursor.execute(query, (id_cancha,))
            return cursor.fetchone()
    finally:
        connection.close()


def get_canchas(filtros, limite, salto):
    connection = get_connection()

    try:
        condiciones = []
        parametros = []

        # Filtro por deporte
        if filtros.get("id_deporte") is not None:
            condiciones.append("id_deporte = %s")
            parametros.append(filtros["id_deporte"])

        # Filtro por nombre
        if filtros.get("nombre") is not None:
            condiciones.append("LOWER(nombre) LIKE %s")
            parametros.append(f"%{filtros['nombre'].lower()}%")

        # Filtro por techada
        if filtros.get("techada") is not None:
            condiciones.append("techada = %s")
            parametros.append(filtros["techada"])

        # Filtro por activa
        if filtros.get("activa") is not None:
            condiciones.append("activa = %s")
            parametros.append(filtros["activa"])

        clausula_where = ""

        if condiciones:
            clausula_where = "WHERE " + " AND ".join(condiciones)

        with connection.cursor() as cursor:
            count_query = f"""
                SELECT COUNT(*) AS total
                FROM canchas
                {clausula_where}
            """

            cursor.execute(count_query, parametros)
            count_result = cursor.fetchone()

            total = (
                count_result["total"]
                if isinstance(count_result, dict)
                else count_result[0]
            )

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
        connection.close()


def get_reserva_by_cancha(id_cancha):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id
                FROM reservas
                WHERE id_cancha = %s
            """

            cursor.execute(query, (id_cancha,))
            return cursor.fetchone()
    finally:
        connection.close()


def delete_cancha(id_cancha):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                DELETE FROM canchas
                WHERE id = %s
            """

            cursor.execute(query, (id_cancha,))

        connection.commit()
    finally:
        connection.close()


def update_cancha(id_cancha, data):
    connection = get_connection()

    try:
        keys = []
        values = []

        for key, value in data.items():
            keys.append(f"{key} = %s")
            values.append(value)

        with connection.cursor() as cursor:
            query = f"""
                UPDATE canchas
                SET {", ".join(keys)}
                WHERE id = %s
            """

            values.append(id_cancha)
            cursor.execute(query, values)

        connection.commit()
    finally:
        connection.close()