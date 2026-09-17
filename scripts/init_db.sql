CREATE DATABASE IF NOT EXISTS club_deportivo;

USE club_deportivo;

CREATE TABLE deportes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);

INSERT INTO deportes (nombre)
VALUES
    ('Futbol'),
    ('Tenis'),
    ('Padel');


CREATE TABLE canchas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL,
    activa BOOLEAN NOT NULL,
    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

CREATE TABLE socios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(250) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha_hora_inicio DATETIME(6) NOT NULL,
    fecha_hora_fin DATETIME(6) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'confirmada',
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,
    FOREIGN KEY (id_socio) REFERENCES socios(id),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id)
);
