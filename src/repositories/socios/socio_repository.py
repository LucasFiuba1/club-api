from db.connection import get_connection


def get_socio_by_id(socio_id):
    connection = get_connection()

    try:
        with connection.cursor(dictonary=True) as cursor:

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
        with connection.cursor() as cursor:

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

        with connection.cursor() as cursor:

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
