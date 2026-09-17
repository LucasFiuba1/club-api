CREATE DATABASE IF NOT EXISTS club_deportivo;

USE club_deportivo;

/* DEPORTES */
CREATE TABLE
    deportes (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(50) NOT NULL UNIQUE
    );

INSERT INTO
    deportes (nombre)
VALUES
    ('Fútbol'),
    ('Tenis'),
    ('Pádel');

-----------------
/* CANCHAS */
CREATE TABLE
    canchas (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        id_deporte INT NOT NULL,
        precio_hora INT NOT NULL,
        techada BOOLEAN NOT NULL DEFAULT FALSE,
        activa BOOLEAN NOT NULL DEFAULT TRUE,
        FOREIGN KEY (id_deporte) REFERENCES deportes (id)
    );

INSERT INTO
    canchas (nombre, id_deporte, precio_hora, techada, activa)
VALUES
    ('Cancha de fútbol 1', 1, 1000000, FALSE, TRUE),
    ('Cancha de Tenis 2', 2, 500000, FALSE, TRUE),
    ('Cancha de Pádel 3', 3, 700000, TRUE, TRUE),
    ('Cancha de Pádel 4', 3, 650000, FALSE, FALSE);

-----------------    
/* SOCIOS */
CREATE TABLE
    socios (
        id INT PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        activo BOOLEAN NOT NULL DEFAULT TRUE
    );

INSERT INTO
    socios (nombre, email, activo)
VALUES
    (
        'Lucas Cirillo Berardi',
        'lucascirilloberardi@gmail.com',
        TRUE
    ),
    ('Joaquin', 'joaquin@gmail.com', TRUE),
    ('Mateo', 'mateo@gmail.com', FALSE),
    ('Roman', 'roman@gmail.com', TRUE),
    ('Sergio', 'sergio@gmail.com', TRUE);

-----------------    
/* RESERVAS */
CREATE TABLE
    reservas (
        id INT PRIMARY KEY AUTO_INCREMENT,
        id_socio INT NOT NULL,
        id_cancha INT NOT NULL,
        fecha_hora_inicio DATETIME (6) NOT NULL,
        fecha_hora_fin DATETIME (6) NOT NULL,
        estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',
        tarifa_hora INT NOT NULL,
        total INT NOT NULL,
        FOREIGN KEY (id_socio) REFERENCES socios (id),
        FOREIGN KEY (id_cancha) REFERENCES canchas (id)
    );

INSERT INTO
    reservas (
        id_socio,
        id_cancha,
        fecha_hora_inicio,
        fecha_hora_fin,
        estado,
        tarifa_hora,
        total
    )
VALUES
    (
        1,
        1,
        '2026-10-15 18:00:00.121000',
        '2026-10-15 20:00:00.121000',
        'confirmada',
        1000000,
        2000000
    );