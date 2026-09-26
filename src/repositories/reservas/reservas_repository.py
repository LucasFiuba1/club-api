from src.db.connection import get_connection


def get_reservas_db(filters, limit, offset):
    connection = get_connection()
    try:
        with connection.cursor(dictionary=True) as cursor:
            conditions = []
            params = []

            if filters.get('id_cancha'):
                conditions.append("id_cancha = %s")
                params.append(filters['id_cancha'])
            if filters.get('id_socio'):
                conditions.append("id_socio = %s")
                params.append(filters['id_socio'])
            if filters.get('estado'):
                conditions.append("estado = %s")
                params.append(filters['estado'])
            if filters.get('fecha_desde'):
                conditions.append("DATE(fecha_hora_inicio) >= %s")
                params.append(filters['fecha_desde'])
            if filters.get('fecha_hasta'):
                conditions.append("DATE(fecha_hora_inicio) <= %s")
                params.append(filters['fecha_hasta'])

            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

            cursor.execute(f"SELECT COUNT(*) as total FROM reservas {where_clause}", params)
            total = cursor.fetchone()['total']

            query = f"SELECT * FROM reservas {where_clause} ORDER BY id ASC LIMIT %s OFFSET %s"
            cursor.execute(query, params + [limit, offset])
            reservas = cursor.fetchall()

            return reservas, total
    finally:
        connection.close()


def get_reserva_by_id(reserva_id):
    connection = get_connection()

    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM reservas WHERE id = %s", (reserva_id,))
            return cursor.fetchone()
    finally:
        connection.close()


def update_estado_db(reserva_id, nuevo_estado):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute("UPDATE reservas SET estado = %s WHERE id = %s", (nuevo_estado, reserva_id))
            connection.commit()
    finally:
        connection.close()

# Prueba
