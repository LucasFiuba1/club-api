from src.db.connection import get_connection


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


def get_deporte_by_id(id_deporte):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT id, nombre
                FROM deportes
                WHERE id = %s
            """

            cursor.execute(query, (id_deporte,))
            return cursor.fetchone()
    finally:
        connection.close()
