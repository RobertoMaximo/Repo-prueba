CREATE DATABASE IF NOT EXISTS mundial;
USE mundial;

CREATE TABLE IF NOT EXISTS fixture (
    id_fixture               INT AUTO_INCREMENT PRIMARY KEY,
    local            VARCHAR(255) DEFAULT NULL,
    visitante        VARCHAR(255) DEFAULT NULL,
    estadio          VARCHAR(255) NOT NULL,
    ciudad           VARCHAR(255) NOT NULL,
    fecha            DATE         NOT NULL,
    fase             VARCHAR(255) NOT NULL,
    goles_local      INT          DEFAULT NULL,
    goles_visitante  INT          DEFAULT NULL
);

-- FASE DE GRUPOS
INSERT INTO fixture (local, visitante, estadio, ciudad, fecha, fase) VALUES
-- Jornada 1


-- Jornada 2
('Republica Checa', 'Sudafrica', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-18', 'Fase de grupos'),
('Suiza', 'Bosnia y Herzegovina', 'SoFi Stadium', 'Los Angeles', '2026-06-18', 'Fase de grupos'),
('Canada', 'Qatar', 'BC Place', 'Vancouver', '2026-06-18', 'Fase de grupos'),
('Mexico', 'Corea del Sur', 'Estadio Guadalajara', 'Guadalajara', '2026-06-18', 'Fase de grupos'),
('Estados Unidos', 'Australia', 'Lumen Field', 'Seattle', '2026-06-19', 'Fase de grupos'),
('Escocia', 'Marruecos', 'Gillette Stadium', 'Boston', '2026-06-19', 'Fase de grupos'),
('Brasil', 'Haiti', 'Lincoln Financial Field', 'Philadelphia', '2026-06-19', 'Fase de grupos'),
('Turquia', 'Paraguay', 'Levi''s Stadium', 'San Francisco', '2026-06-19', 'Fase de grupos'),
('Paises Bajos', 'Suecia', 'NRG Stadium', 'Houston', '2026-06-20', 'Fase de grupos'),
('Alemania', 'Costa de Marfil', 'BMO Field', 'Toronto', '2026-06-20', 'Fase de grupos'),
('Ecuador', 'Curazao', 'Arrowhead Stadium', 'Kansas City', '2026-06-20', 'Fase de grupos'),
('Tunez', 'Japon', 'Estadio BBVA', 'Monterrey', '2026-06-20', 'Fase de grupos'),
('Espana', 'Arabia Saudita', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-21', 'Fase de grupos'),
('Belgica', 'Iran', 'SoFi Stadium', 'Los Angeles', '2026-06-21', 'Fase de grupos'),
('Uruguay', 'Cabo Verde', 'Hard Rock Stadium', 'Miami', '2026-06-21', 'Fase de grupos'),
('Nueva Zelanda', 'Egipto', 'BC Place', 'Vancouver', '2026-06-21', 'Fase de grupos'),
('Argentina', 'Austria', 'AT&T Stadium', 'Dallas', '2026-06-22', 'Fase de grupos'),
('Francia', 'Irak', 'Lincoln Financial Field', 'Philadelphia', '2026-06-22', 'Fase de grupos'),
('Noruega', 'Senegal', 'MetLife Stadium', 'Nueva York', '2026-06-22', 'Fase de grupos'),
('Jordania', 'Argelia', 'Levi''s Stadium', 'San Francisco', '2026-06-22', 'Fase de grupos'),
('Portugal', 'Uzbekistan', 'NRG Stadium', 'Houston', '2026-06-23', 'Fase de grupos'),
('Inglaterra', 'Ghana', 'Gillette Stadium', 'Boston', '2026-06-23', 'Fase de grupos'),
('Panama', 'Croacia', 'BMO Field', 'Toronto', '2026-06-23', 'Fase de grupos'),
('Colombia', 'Rep. Democratica del Congo', 'Estadio Guadalajara', 'Guadalajara', '2026-06-23', 'Fase de grupos'),

-- Jornada 3
('Suiza', 'Canada', 'BC Place', 'Vancouver', '2026-06-24', 'Fase de grupos'),
('Bosnia y Herzegovina', 'Qatar', 'Lumen Field', 'Seattle', '2026-06-24', 'Fase de grupos'),
('Escocia', 'Brasil', 'Hard Rock Stadium', 'Miami', '2026-06-24', 'Fase de grupos'),
('Marruecos', 'Haiti', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-24', 'Fase de grupos'),
('Republica Checa', 'Mexico', 'Estadio Azteca', 'Ciudad de Mexico', '2026-06-24', 'Fase de grupos'),
('Sudafrica', 'Corea del Sur', 'Estadio BBVA', 'Monterrey', '2026-06-24', 'Fase de grupos'),
('Ecuador', 'Alemania', 'MetLife Stadium', 'Nueva York', '2026-06-25', 'Fase de grupos'),
('Curazao', 'Costa de Marfil', 'Lincoln Financial Field', 'Philadelphia', '2026-06-25', 'Fase de grupos'),
('Tunez', 'Paises Bajos', 'Arrowhead Stadium', 'Kansas City', '2026-06-25', 'Fase de grupos'),
('Japon', 'Suecia', 'AT&T Stadium', 'Dallas', '2026-06-25', 'Fase de grupos'),
('Turquia', 'Estados Unidos', 'SoFi Stadium', 'Los Angeles', '2026-06-25', 'Fase de grupos'),
('Paraguay', 'Australia', 'Levi''s Stadium', 'San Francisco', '2026-06-25', 'Fase de grupos'),
('Noruega', 'Francia', 'Gillette Stadium', 'Boston', '2026-06-26', 'Fase de grupos'),
('Senegal', 'Irak', 'BMO Field', 'Toronto', '2026-06-26', 'Fase de grupos'),
('Uruguay', 'Espana', 'Estadio Guadalajara', 'Guadalajara', '2026-06-26', 'Fase de grupos'),
('Cabo Verde', 'Arabia Saudita', 'NRG Stadium', 'Houston', '2026-06-26', 'Fase de grupos'),
('Nueva Zelanda', 'Belgica', 'BC Place', 'Vancouver', '2026-06-26', 'Fase de grupos'),
('Egipto', 'Iran', 'Lumen Field', 'Seattle', '2026-06-26', 'Fase de grupos'),
('Panama', 'Inglaterra', 'MetLife Stadium', 'Nueva York', '2026-06-27', 'Fase de grupos'),
('Croacia', 'Ghana', 'Lincoln Financial Field', 'Philadelphia', '2026-06-27', 'Fase de grupos'),
('Colombia', 'Portugal', 'Hard Rock Stadium', 'Miami', '2026-06-27', 'Fase de grupos'),
('Rep. Democratica del Congo', 'Uzbekistan', 'Mercedes-Benz Stadium', 'Atlanta', '2026-06-27', 'Fase de grupos'),
('Jordania', 'Argentina', 'AT&T Stadium', 'Dallas', '2026-06-27', 'Fase de grupos'),
('Argelia', 'Austria', 'Arrowhead Stadium', 'Kansas City', '2026-06-27', 'Fase de grupos');


CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE Predicciones(
    id_fixture INT,
    id_usuario int,
    goles_local INT,
    goles_visitante VARCHAR(30),
    FOREIGN KEY (id_fixture) REFERENCES fixture(id_fixture) ON DELETE CASCADE
);
