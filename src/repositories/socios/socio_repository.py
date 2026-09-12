from db.connection import get_connection


def get_socio_by_id(socio_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT id, email, nombre, activo 
                FROM socios 
                WHERE id = %s", 
            """

            cursor.execute(query, socio_id)
            
            return cursor.fetchone()
    finally: 
        connection.close()
