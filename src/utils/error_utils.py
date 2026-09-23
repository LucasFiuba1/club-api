def build_error(code, message, description):
    return {
        "errors": [
            {
                "code": code,
                "message": message,
                "level": "error",
                "description": description,
            }
        ]
    }


def socio_not_found_error(socio_id):
    return build_error(
        "SOCIO_NO_ENCONTRADO",
        "Socio no encontrado.",
        f"No existe un socio con id: {socio_id}",
    )

def socio_inactive_error(socio_id):
    return build_error(
        "SOCIO_INACTIVO",
        "El socio no está activo",
        f"El socio con id: {socio_id} no está activo",
    )

def cancha_not_found_error(cancha_id):
    return build_error(
        "CANCHA_NO_ENCONTRADA",
        "Cancha no encontrada.",
        f"No existe una cancha con el id: {cancha_id}",
    )

def cancha_inactive_error(cancha_id):
    return build_error(
        "CANCHA_INACTIVA",
        "La cancha no está activa",
        f"La cancha con id: {cancha_id} no está activa",
    )

def cancha_overlap_error(id_cancha, fecha, hora_inicio, hora_fin):
    return build_error(
        "SOLAPAMIENTO_CANCHA",
        "La cancha ya está reservada en ese horario",
        f"La cancha {id_cancha} ya tiene una reserva confirmada entre {hora_inicio}-{hora_fin} el día {fecha}",
    )

def time_not_top_of_hour_error(hora):
    return build_error(
        "HORA_INVALIDA",
        "La hora debe ser en punto.",
        f"La hora {hora} no está en punto",
    )

def time_out_of_range_error(hora):
    return build_error(
        "HORA_FUERA_DEL_RANGO",
        "La hora debe estar en el rango 08:00 a 23:00",
        f"La hora {hora} está fuera del rango permitido (08:00-23:00)",
    )

def invalid_reservation_duration_error(duracion_reserva):
    return build_error(
        "DURACION_RESERVA_FUERA_DEL_RANGO",
        "La duracion de la reserva debe estar en el rango 1 a 3 horas",
        f"La duracion {duracion_reserva} está fuera del rango permitido (1-3)",
    )

def reserva_not_future_error(fecha_hora_inicio):
    return build_error(
        "RESERVA_NO_FUTURA",
        "El inicio de la reserva debe ser posterior al momento actual.",
        f"La fecha y la hora de inicio {fecha_hora_inicio} ya pasó o es el momento actual."
    )