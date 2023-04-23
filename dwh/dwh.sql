DROP DATABASE IF EXISTS FlightDWH;
CREATE DATABASE FlightDWH;
USE FlightDWH; 
SET SQL_SAFE_UPDATES = 0;

-- sterschema moet aangepast worden

-- ----------------------------------------------------------------------------------------------------------
-- Maak DimAirport
CREATE TABLE IF NOT EXISTS FlightDWH.DimAirport(
    AirportKey INT NOT NULL AUTO_INCREMENT, -- nog veranderen naar andere key dan auto_increment!
    AirportCode CHAR(3) UNIQUE NOT NULL,
    AirportName VARCHAR(50),
    City VARCHAR(50),
    Country VARCHAR(50),
    DistanceFlown INT,
    PRIMARY KEY (AirportKey),
    FOREIGN KEY (DistanceFlown) REFERENCES FlightDWH.DimAirport(AirportKey)
);

-- Update reeds bestaande records
UPDATE FlightDWH.DimAirport dima SET 
AirportCode = (SELECT iata FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode),
AirportName = (SELECT name FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode),
City = (SELECT city FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode),
Country = (SELECT country FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode);

-- Insert nieuwe records
INSERT INTO FlightDWH.DimAirport (AirportCode, AirportName, City, Country)
SELECT DISTINCT iata, name, city, country
FROM flight_oltp.flight_airport
WHERE iata NOT IN (SELECT DISTINCT AirportCode FROM FlightDWH.DimAirport);

-- ----------------------------------------------------------------------------------------------------------
-- Maak DimAirline
CREATE TABLE IF NOT EXISTS FlightDWH.DimAirline (
  AirlineKey INT NOT NULL AUTO_INCREMENT, -- nog veranderen naar andere key dan auto_increment!
  AirlineCode CHAR(3) UNIQUE,
  AirlineName VARCHAR(50),
  AirlineContact VARCHAR(50),
  AirlineAddress VARCHAR(100),
  PRIMARY KEY (AirlineKey)
);

-- Update reeds bestaande records
UPDATE FlightDWH.DimAirline dima SET 
AirlineCode = (SELECT iata FROM flight_oltp.flight_airline flighta WHERE flighta.iata = dima.AirlineCode),
AirlineName = (SELECT name FROM flight_oltp.flight_airline flighta WHERE flighta.name = dima.AirlineName);

-- Insert nieuwe records
INSERT INTO FlightDWH.DimAirline (AirlineCode, AirlineName)
SELECT DISTINCT iata, name
FROM flight_oltp.flight_airline
WHERE iata NOT IN (SELECT DISTINCT AirlineCode FROM FlightDWH.DimAirline);

-- Extra informatie buiten de OLTP database
UPDATE FlightDWH.DimAirline SET
AirlineContact = '+32 2 723 23 62', 
AirlineAddress = 'Jaargetijdenlaan 100-102, 1050 Elsene, België'
WHERE AirlineCode = 'SN';

UPDATE FlightDWH.DimAirline SET
AirlineContact = '+32 7 066 03 05 ', 
AirlineAddress = 'Piet Guilonardweg 15 1117 EE Schiphol'
WHERE AirlineCode = 'HV';

UPDATE FlightDWH.DimAirline SET
AirlineContact = '+32 2 717 86 61', 
AirlineAddress = 'Luchthaven Brussel Nationaal, 40 Bus 1, 1930 Zaventem, België'
WHERE AirlineCode = 'TB';

UPDATE FlightDWH.DimAirline SET
AirlineContact = '+32 7 848 21 30', 
AirlineAddress = 'Airside Business Park, Swords, Co. Dublin,Ireland'
WHERE AirlineCode = 'FR';