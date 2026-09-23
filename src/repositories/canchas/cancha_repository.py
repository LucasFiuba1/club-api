from db.connection import get_connection


def get_cancha_by_id(cancha_id):
    connection=get_connection()
    
    try:
        with connection.cursor(dictionary=True) as cursor:
            query= """
                SELECT id, nombre, id_deporte, precio_hora, techada, activa
                FROM canchas
                WHERE id=%s
            """
            cursor.execute(query, (cancha_id,))
            return cursor.fetchone()
    finally:
        connection.close()

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