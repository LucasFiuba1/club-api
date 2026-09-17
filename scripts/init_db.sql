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
    canchas (nombre, precio_hora, techada, activa)
VALUES
    (
        ('Cancha de fútbol 1', 1, 1000000, FALSE, TRUE),
        ('Cancha de Tenis 2', 2, 500000, FALSE, TRUE),
        ('Cancha de Pádel 3', 3, 700000, TRUE, TRUE),
        ('Cancha de Pádel 3', 3, 650000, FALSE, FALSE)
    );
