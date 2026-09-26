from src.db.connection import get_connection


def get_socio_by_id(socio_id):
    connection = get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:

            query = """
                SELECT id, email, nombre, activo 
                FROM socios 
                WHERE id = %s
            """

            cursor.execute(query, (socio_id,))

            return cursor.fetchone()
    finally:
        connection.close()


def get_socio_by_email(socio_email):
    connection = get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:

            query = """
                SELECT id, email, nombre, activo 
                FROM socios 
                WHERE email = %s 
            """

            cursor.execute(query, (socio_email,))

            return cursor.fetchone()
    finally:
        connection.close()


def update_socio(socio_id, data):
    connection = get_connection()

    try:
        keys = []
        values = []

        for key, value in data.items():
            keys.append(f"{key} = %s")
            values.append(value)

        with connection.cursor(dictionary=True) as cursor:

            query = f"""
                UPDATE socios 
                SET {", " .join(keys)}
                WHERE id = %s
            """

            values.append(socio_id)

            cursor.execute(query, values)

            connection.commit()
    finally:
        connection.close()


def create_socio(data):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        query = """
                INSERT INTO socios (nombre, email, activo)
                VALUES (%s, %s, %s)
            """

        values = (
                data["nombre"],
                data["email"],
                data["activo"]
            )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()

    except Exception:
        connection.rollback()
        raise

    finally:
            connection.close()


def get_socios(filtros, limit, offset):
    connection = get_connection()

    try:
        conditions = []
        parameters = []

        if "nombre" in filtros:
            conditions.append("LOWER(nombre) LIKE %s")
            parameters.append("%" + filtros["nombre"].lower() + "%")

        if "activo" in filtros:
            conditions.append("activo = %s")
            parameters.append(filtros["activo"])

        where = ""

        if conditions:
            where = "WHERE " + " AND ".join(conditions)

        cursor = connection.cursor(dictionary=True)

        count_query = f"""
            SELECT COUNT(*) AS total
            FROM socios
            {where}
        """

        cursor.execute(count_query, tuple(parameters))
        total = cursor.fetchone()["total"]

        query = f"""
            SELECT id, nombre, email, activo
            FROM socios
            {where}
            ORDER BY id ASC
            LIMIT %s OFFSET %s
        """

        page_parameters = parameters.copy()
        page_parameters.append(limit)
        page_parameters.append(offset)

        cursor.execute(query, tuple(page_parameters))

        socios = cursor.fetchall()

        for socio in socios:
            socio["activo"] = bool(socio["activo"])

        cursor.close()
        return socios, total

    finally:
        connection.close()
