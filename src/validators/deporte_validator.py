def validate_deporte_id(id_deporte):
    try: 
        val = int(id_deporte)
    except (ValueError, TypeError):
        return False, 
    if val <= 0:
        return False,
    return True, None