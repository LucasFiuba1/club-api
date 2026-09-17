from db.connection import get_connection

def get_deporte_by_id(id_deporte):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id
                FROM deportes
                WHERE id = %s
            """
            cursor.execute(query, (id_deporte,))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()

def create_cancha(data):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """

                INSERT INTO canchas (
                nombre, id_deporte, precio_hora, techada, activa
            )
            VALUES (%s, %s, %s, %s, %s)

            """
            cursor.execute(
                query,
                (
                    data["nombre"],
                    data["id_deporte"],
                    data["precio_hora"],
                    data["techada"],
                    data["activa"]

                )
            )

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
            result = cursor.fetchone()
            return result
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
            result = cursor.fetchone()
            return result
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


