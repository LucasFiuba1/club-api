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
