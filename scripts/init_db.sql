CREATE DATABASE IF NOT EXISTS club_deportivo;

USE club_deportivo;

CREATE TABLE IF NOT EXISTS deportes (
    
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    
);

CREATE TABLE IF NOT EXISTS canchas (
    
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    id_deporte INT NOT NULL,
    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);

insert into deportes (nombre) 
values 
    ('Futbol'),
    ('Tenis'),
    ('Padel');



insert into canchas (nombre, id_deporte, precio_hora, techada, activa)
values 
    ('Cancha Principal 11', 1, 150, FALSE, TRUE),
    ('Cancha Sintetico 5',  1, 100, TRUE,  TRUE),
    ('Cancha Polvo de Ladrillo 1', 2, 12, FALSE, TRUE),
    ('Cancha Rapida Techada',     2, 14, TRUE,  TRUE),
    ('Cancha Padel Cristal',       3,  90, TRUE,  TRUE),
    ('Cancha Padel Descubierta',   3,  75, FALSE, FALSE);