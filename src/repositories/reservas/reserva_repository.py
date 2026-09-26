from src.db.connection import get_connection


def existe_superposicion(id_cancha, fecha, hora_inicio, hora_fin):
    connection=get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:
            query="""
                SELECT 1
                FROM reservas
                WHERE reservas.id_cancha = %s
                    AND reservas.estado = 'confirmada'
                    AND reservas.fecha_hora_inicio < CONCAT(%s, ' ', %s)
                    AND reservas.fecha_hora_fin > CONCAT(%s, ' ', %s)
            """
            cursor.execute(query, (id_cancha, fecha, hora_fin, fecha, hora_inicio,))
            return cursor.fetchone() is not None
    finally:
        connection.close()

def existe_superposicion_socio(id_socio, fecha, hora_inicio, hora_fin):
    connection=get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:
            query="""
                SELECT 1
                FROM reservas
                WHERE reservas.id_socio = %s
                    AND reservas.estado = 'confirmada'
                    AND reservas.fecha_hora_inicio < CONCAT(%s, ' ', %s)
                    AND reservas.fecha_hora_fin > CONCAT(%s, ' ',%s)
            """
            cursor.execute(query, (id_socio, fecha, hora_fin, fecha, hora_inicio,))
            return cursor.fetchone() is not None
    finally:
        connection.close()

def create_reserva(id_socio, id_cancha,fecha_hora_inici, fecha_hora_fin, estado, precio_hora, precio_total):
    connection=get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:
            query="""
                INSERT INTO reservas(id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
                VALUES (%s, %s, %s, %s, %s,%s, %s)
            """
            cursor.execute(query, (id_socio, id_cancha, fecha_hora_inici, fecha_hora_fin, estado, precio_hora, precio_total,))
            connection.commit()
            return cursor.lastrowid
    finally:
        connection.close()