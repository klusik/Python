CREATE TABLE lidi (
  id_lidi INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  jmeno VARCHAR(255) NOT NULL,
  prijmeni VARCHAR(255) NOT NULL,
  rok_narozeni INTEGER NOT NULL
);

INSERT INTO lidi (id_lidi, jmeno, prijmeni, rok_narozeni) VALUES
(1, 'Rudolf', 'Klusal', 1984),
(2, 'Dagmar', 'Kodýtková', 1982),
(3, 'Kateřina', 'Chejlavová', 1990),
(4, 'Michal', 'Sýkora', 1985),
(5, 'Daniel', 'Krudenc', 1982),
(6, 'Marie', 'Částková', 1919),
(7, 'Ladislav', 'Matonoha', 1952),
(8, 'Rudolf', 'Klusal', 1956);

CREATE TABLE lidi_pribory (
  id_lidi_pribory INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  id_pribory INTEGER NOT NULL,
  id_lidi INTEGER NOT NULL,
  pocet INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY (id_lidi) REFERENCES lidi (id_lidi),
  FOREIGN KEY (id_pribory) REFERENCES pribory (id_pribory)
);

INSERT INTO lidi_pribory (id_lidi_pribory, id_pribory, id_lidi, pocet) VALUES
(1, 1, 1, 10),
(2, 1, 2, 15),
(3, 1, 3, 5),
(4, 2, 1, 10),
(5, 3, 5, 12),
(6, 4, 5, 1),
(7, 5, 1, 5),
(8, 5, 2, 7),
(9, 5, 3, 15),
(10, 5, 4, 2),
(11, 5, 5, 15),
(12, 5, 6, 13),
(13, 5, 7, 9),
(14, 5, 8, 8),
(15, 6, 1, 2),
(16, 6, 2, 3),
(17, 6, 3, 14),
(18, 6, 4, 13),
(19, 6, 5, 11),
(20, 6, 6, 17),
(21, 6, 8, 7),
(22, 6, 7, 7);

CREATE TABLE materialy (
  id_material INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  material VARCHAR(255) NOT NULL,
  hustota REAL NOT NULL DEFAULT 1
);

INSERT INTO materialy (id_material, material, hustota) VALUES
(1, 'voda', 1),
(2, 'vzduch', 0.01),
(3, 'železo', 5),
(4, 'dřevo', 0.7),
(5, 'sklo', 2.2);

CREATE TABLE pribory (
  id_pribory INTEGER PRIMARY KEY AUTOINCREMENT,
  nazev TEXT NOT NULL,
  id_material INTEGER NOT NULL,
  UNIQUE(nazev, id_material),
  FOREIGN KEY (id_material) REFERENCES materialy(id_material)
);

INSERT INTO pribory (id_pribory, nazev, id_material) VALUES
(3, 'lžíce', 3),
(6, 'lžíce', 5),
(7, 'nůž', 5),
(4, 'příborový nůž', 3),
(1, 'vidlička', 3),
(2, 'vidlička', 4),
(5, 'vidlička', 5);
