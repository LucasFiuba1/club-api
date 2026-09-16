CREATE DATABASE IF NOT EXISTS club_deportivo;

USE club_deportivo;

CREATE TABLE deportes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL
);



CREATE TABLE canchas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL, 
    id_deporte INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL,
    activa BOOLEAN NOT NULL,
    FOREIGN KEY (id_deporte) REFERENCES deportes(id)
);
