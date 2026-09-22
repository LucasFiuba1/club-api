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

CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha_hora_inicio DATETIME NOT NULL,
    fecha_hora_fin DATETIME NOT NULL, 
    estado VARCHAR(50) NOT NULL DEFAULT 'confirmada',
    tarifa_hora BIGINT NOT NULL,
    importe_total BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_socio) REFERENCES socios(id),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id)
);
/*fila de prueba*/
INSERT INTO reservas(id_socio, id_cancha, fecha_hora_inicio, fecha_hora_fin, estado, tarifa_hora, importe_total)
VALUES (1, 2, '2026-10-15 18:00:00', '2026-10-15 20:00:00', 'confirmada', 1000000, 2000000);