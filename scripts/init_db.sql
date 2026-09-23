CREATE DATABASE IF NOT EXISTS club_deportivo;

USE club_deportivo;

CREATE TABLE IF NOT EXISTS deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(250) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL,
    activa BOOLEAN NOT NULL,
    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);


CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha_hora_inicio DATETIME(6) NOT NULL,
    fecha_hora_fin DATETIME(6) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,
    FOREIGN KEY (id_cancha) REFERENCES canchas(id),
    FOREIGN KEY (id_socio) REFERENCES socios(id)
);

INSERT INTO deportes (nombre)
VALUES 
    ('Futbol'),
    ('Padel'),
    ('Tenis');

INSERT INTO canchas (nombre, id_deporte, precio_hora, techada, activa)
VALUES
    ('Cancha 1 - Futbol 5', 1, 1000000, FALSE, TRUE),
    ('Cancha 2 - Padel', 2, 1200000, TRUE, TRUE),
    ('Cancha 3 - Tenis', 3, 1250000, FALSE, FALSE);

INSERT INTO socios (nombre, email, activo)
VALUES
    ('Juan Perez', 'juanpe@ejemplo.com', TRUE),
    ('Alberto Carlos', 'beto@ejemplo.com', FALSE),
    ('Diego Ruiz', 'dieguito5@ejemplo.com', TRUE);

INSERT INTO reservas(id_cancha, id_socio, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
VALUES
    (1, 1, '2026-10-15 18:00:00.000000', '2026-10-15 20:00:00.000000', 'confirmada', 1000000, 2000000);