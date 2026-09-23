from db.connection import get_connection


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