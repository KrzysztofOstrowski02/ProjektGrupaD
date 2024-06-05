-- Tworzenie tabeli Klienci
CREATE TABLE Klienci (
    KlientID INTEGER PRIMARY KEY,
    Imie TEXT NOT NULL,
    Nazwisko TEXT NOT NULL,
    Email TEXT NOT NULL,
    Telefon TEXT NOT NULL
);

-- Dodanie rekordów do tabeli Klienci
INSERT INTO Klienci (Imie, Nazwisko, Email, Telefon) VALUES
('Jan', 'Kowalski', 'jan.kowalski@interia.pl', '123456789'),
('Anna', 'Nowak', 'anna.nowak@interia.pl', '987654321'),
('Piotr', 'Wiśniewski', 'piotr.wisniewski@onet.pl', '555123456'),
('Maria', 'Wójcik', 'maria.wojcik@gmail.com', '444567890'),
('Krzysztof', 'Kowalczyk', 'krzysztof.kowalczyk@gmail.com', '333789012');

-- Tworzenie tabeli Samochody
CREATE TABLE Samochody (
    SamochodID INTEGER PRIMARY KEY,
    Marka TEXT NOT NULL,
    Model TEXT NOT NULL,
    Rok INTEGER NOT NULL,
    Cena REAL NOT NULL
);

-- Dodanie rekordów do tabeli Samochody
INSERT INTO Samochody (Marka, Model, Rok, Cena) VALUES
('Toyota', 'Camry', 2020, 24000),
('Honda', 'Civic', 2019, 20000),
('Ford', 'Mustang', 2021, 30000),
('Chevrolet', 'Malibu', 2018, 18000),
('Nissan', 'Altima', 2022, 25000);

-- Tworzenie tabeli Sprzedawcy
CREATE TABLE Sprzedawcy (
    SprzedawcaID INTEGER PRIMARY KEY,
    Imie TEXT NOT NULL,
    Nazwisko TEXT NOT NULL,
    Email TEXT NOT NULL,
    Telefon TEXT NOT NULL
);

-- Dodanie rekordów do tabeli Sprzedawcy
INSERT INTO Sprzedawcy (Imie, Nazwisko, Email, Telefon) VALUES
('Alicja', 'Jankowska', 'alicja.jankowska@sklep.com', '123123123'),
('Bartłomiej', 'Wiśniewski', 'bartlomiej.wisniewski@sklep.com', '321321321'),
('Karolina', 'Kowalska', 'karolina.kowalska@sklep.com', '456456456'),
('Dawid', 'Nowak', 'dawid.nowak@sklep.com', '654654654'),
('Ewa', 'Kamińska', 'ewa.kaminska@sklep.com', '789789789');

-- Tworzenie tabeli Sprzedaze
CREATE TABLE Sprzedaze (
    SprzedazID INTEGER PRIMARY KEY,
    KlientID INTEGER NOT NULL,
    SamochodID INTEGER NOT NULL,
    SprzedawcaID INTEGER NOT NULL,
    DataSprzedazy TEXT NOT NULL,
    FOREIGN KEY (KlientID) REFERENCES Klienci(KlientID),
    FOREIGN KEY (SamochodID) REFERENCES Samochody(SamochodID),
    FOREIGN KEY (SprzedawcaID) REFERENCES Sprzedawcy(SprzedawcaID)
);

-- Dodanie rekordów do tabeli Sprzedaze
INSERT INTO Sprzedaze (KlientID, SamochodID, SprzedawcaID, DataSprzedazy) VALUES
(1, 3, 2, '2023-01-15'),
(2, 1, 1, '2023-02-20'),
(3, 5, 3, '2023-03-25'),
(4, 2, 4, '2023-04-30'),
(5, 4, 5, '2023-05-05');
