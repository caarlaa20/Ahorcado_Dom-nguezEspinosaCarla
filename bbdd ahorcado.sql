DROP DATABASE IF EXISTS juegoahorcado;
CREATE DATABASE JuegoAhorcado;
USE JuegoAhorcado;


CREATE TABLE categoría (
  id_fruta INT,
  id_informatica INT,
  id_nombre INT
);

CREATE TABLE Fruta (
  id_fruta INT,
  nombre VARCHAR(200)
);

CREATE TABLE Informatica (
  id_informatica INT,
  nombre VARCHAR(200)
);

CREATE TABLE Nombres (
  id_nombre INT,
  nombre VARCHAR(200)
);

CREATE TABLE jugadores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  partidas_ganadas INT DEFAULT 0,
  partidas_perdidas INT DEFAULT 0
);


INSERT INTO Nombres (id_nombre, nombre) VALUES
(1, 'carlos'),
(2, 'maria'),
(3, 'juan'),
(4, 'ana'),
(5, 'luis'),
(6, 'sofia'),
(7, 'jorge'),
(8, 'elena'),
(9, 'pedro'),
(10, 'lucia'),
(11, 'miguel'),
(12, 'isabel'),
(13, 'diego'),
(14, 'carmen'),
(15, 'fernando'),
(16, 'claudia'),
(17, 'raul'),
(18, 'adriana'),
(19, 'ricardo'),
(20, 'victoria');


INSERT INTO Fruta (id_fruta, nombre) VALUES
(1, 'manzana'),
(2, 'banana'),
(3, 'naranja'),
(4, 'fresa'),
(5, 'uva'),
(6, 'mango'),
(7, 'pina'),
(8, 'papaya'),
(9, 'kiwi'),
(10, 'melon'),
(11, 'sandia'),
(12, 'cereza'),
(13, 'durazno'),
(14, 'pera'),
(15, 'lima'),
(16, 'limon'),
(17, 'frambuesa'),
(18, 'arandano'),
(19, 'granada'),
(20, 'guayaba');


INSERT INTO Informatica (id_informatica, nombre) VALUES
(1, 'computadora'),
(2, 'teclado'),
(3, 'mouse'),
(4, 'monitor'),
(5, 'impresora'),
(6, 'escanner'),
(7, 'servidor'),
(8, 'laptop'),
(9, 'tablet'),
(10, 'smartphone'),
(11, 'cable'),
(12, 'router'),
(13, 'switch'),
(14, 'disco'),
(15, 'memoria'),
(16, 'altavoces'),
(17, 'auriculares'),
(18, 'procesador'),
(19, 'placa'),
(20, 'fuente');


-- SELECT * FROM Fruta;
-- SELECT * FROM jugadores;
