DROP DATABASE IF EXISTS FlightDWH;
CREATE DATABASE FlightDWH;
USE FlightDWH; 
SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- sterschema moet aangepast worden

-- ----------------------------------------------------------------------------------------------------------
-- Maak DimAirport
CREATE TABLE IF NOT EXISTS FlightDWH.DimAirport(
    AirportCode CHAR(3) UNIQUE NOT NULL,
    AirportName VARCHAR(50),
    City VARCHAR(50),
    Country VARCHAR(50),
    PRIMARY KEY (AirportCode)
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
  AirlineCode CHAR(3) UNIQUE NOT NULL,
  AirlineName VARCHAR(50),
  AirlineContact VARCHAR(50),
  AirlineAddress VARCHAR(100),
  PRIMARY KEY (AirportCode)
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


-- ----------------------------------------------------------------------------------------------------------
-- Tijdelijke tabellen voor kleine en gewone nummers
DROP TABLE IF EXISTS FlightDWH.numbers_small;
CREATE TABLE FlightDWH.numbers_small (number INT);
INSERT INTO FlightDWH.numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

DROP TABLE IF EXISTS FlightDWH.numbers;
CREATE TABLE FlightDWH.numbers (number BIGINT);
INSERT INTO FlightDWH.numbers
SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number
FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones
LIMIT 1000000;


-- ----------------------------------------------------------------------------------------------------------
-- Maak DimDate
CREATE TABLE FlightDWH.DimDate (
  DateKey DATE,
  FullDateAlternateKey DATETIME,
  EnglishDayNameOfWeek VARCHAR(10),
  DutchDayNameOfWeek VARCHAR(50),
  DayOfWeek TINYINT,
  DayOfMonth TINYINT,
  DayOfYear SMALLINT,
  WeekOfMonth TINYINT,
  WeekOfYear TINYINT,
  MonthOfYear TINYINT,
  EnglishMonthName VARCHAR(10),
  DutchMonthName VARCHAR(10),
  Quarter TINYINT,
  Year SMALLINT,
  Holiday BOOLEAN,
  NameHoliday VARCHAR(50),
  BelgianVacation varchar(50),
  -- Weekend VARCHAR(10),
  Weekend BOOLEAN, 
  UNIQUE KEY `FullDateAlternateKey` (`FullDateAlternateKey`)
);

ALTER TABLE FlightDWH.DimDate
ADD INDEX idx_DateKey (DateKey);

-- Vul datekey en alternate key aan
INSERT INTO FlightDWH.DimDate (DateKey, FullDateAlternateKey)
SELECT DATE(date_add('2023-01-01', INTERVAL number DAY)), date_add('2023-01-01', INTERVAL number DAY)
FROM numbers
WHERE DATE_ADD( '2023-01-01', INTERVAL number DAY ) BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY number;


-- Vul DimDate (datekey en alternate key zijn al aangevuld)
UPDATE FlightDWH.DimDate SET
EnglishDayNameOfWeek=DAYNAME(FullDateAlternateKey),
DutchDayNameOfWeek	=CASE
						WHEN EnglishDayNameOfWeek IN ('Monday') THEN 'Maandag'
						WHEN EnglishDayNameOfWeek IN ('Tuesday') THEN 'Dinsdag'
						WHEN EnglishDayNameOfWeek IN ('Wednesday') THEN 'Woensdag'
						WHEN EnglishDayNameOfWeek IN ('Thursday') THEN 'Donderdag'
						WHEN EnglishDayNameOfWeek IN ('Friday') THEN 'Vrijdag'
						WHEN EnglishDayNameOfWeek IN ('Saturday') THEN 'Zaterdag'
						WHEN EnglishDayNameOfWeek IN ('Sunday') THEN 'Zondag'
						ELSE NULL
						END,
DayOfWeek     	= WEEKDAY(FullDateAlternateKey)+1,
DayOfMonth    	= DATE_FORMAT( FullDateAlternateKey, '%d' ),
DayOfYear     	= DATE_FORMAT( FullDateAlternateKey, '%j' ),
WeekOfMonth		= FLOOR((DayOfMonth(FullDateAlternateKey)-1)/7)+1,
WeekOfYear    	= DATE_FORMAT( FullDateAlternateKey, '%V' ),
MonthOfYear   	= DATE_FORMAT( FullDateAlternateKey, '%m'),
EnglishMonthName= DATE_FORMAT( FullDateAlternateKey, '%M'),
DutchMonthName	= CASE
					WHEN EnglishMonthName = 'January' THEN 'Januari'
					WHEN EnglishMonthName = 'February' THEN 'Februari'
					WHEN EnglishMonthName = 'March' THEN 'Maart'
					WHEN EnglishMonthName = 'April' THEN 'April'
					WHEN EnglishMonthName = 'May' THEN 'Mei'
					WHEN EnglishMonthName = 'June' THEN 'Juni'
					WHEN EnglishMonthName = 'July' THEN 'Juli'
					WHEN EnglishMonthName = 'August' THEN 'Augustus'
					WHEN EnglishMonthName = 'September' THEN 'September'
					WHEN EnglishMonthName = 'October' THEN 'Oktober'
					WHEN EnglishMonthName = 'November' THEN 'November'
					WHEN EnglishMonthName = 'December' THEN 'December'
					ELSE NULL
					END,
Quarter         = QUARTER(FullDateAlternateKey), 
Year            = DATE_FORMAT( FullDateAlternateKey, "%Y" ),
NameHoliday 	= CASE 
					WHEN (DayOfMonth = 1 AND MonthOfYear = 1) THEN 'Nieuwjaar'
					WHEN (DayOfMonth = 10 AND MonthOfYear = 4) THEN 'Paasmaandag'
					WHEN (DayOfMonth = 1 AND MonthOfYear = 5) THEN 'Dag van de Arbeid'
					WHEN (DayOfMonth = 18 AND MonthOfYear = 5) THEN 'O.H. Hemelvaart'
					WHEN (DayOfMonth = 29 AND MonthOfYear = 5) THEN 'Pinkstermaandag'
					WHEN (DayOfMonth = 21 AND MonthOfYear = 7) THEN 'Nationale feestdag'
					WHEN (DayOfMonth = 15 AND MonthOfYear = 8) THEN 'O.L.V. hemelvaart'
					WHEN (DayOfMonth = 1 AND MonthOfYear = 11) THEN 'Allerheiligen'
					WHEN (DayOfMonth = 11 AND MonthOfYear = 11) THEN 'Wapenstilstand'
					WHEN (DayOfMonth = 25 AND MonthOfYear = 12) THEN 'Kerstmis'
					ELSE NULL
					-- ELSE 'Geen Feestdag'
					-- Holiday = IF(NameHoliday <> 'Geen Feestdag', True, False),
					END,
-- specifiek voor 2023, nu hard coded, kan aangepast worden met aparte table voor holidays om future proof te maken
BelgianVacation = CASE 
					WHEN ((DayOfMonth <= 8 AND MonthOfYear = 1) OR (DayOfMonth >= 25 AND MonthOfYear = 12)) THEN 'Kerstvakantie'
					WHEN (DayOfMonth >= 3 AND DayOfMonth <= 16 AND  MonthOfYear = 4) THEN 'Paasvakantie'
					WHEN (DayOfMonth <= 31 AND (MonthOfYear = 7 OR MonthOfYear = 8)) THEN 'Zomervakantie'
					WHEN ((DayOfMonth >= 30 AND MonthOfYear = 10) OR (DayOfMonth <= 5 AND MonthOfYear = 11)) THEN 'O.H. Hemelvaart'
					ELSE NULL
					END,
Holiday 		= IF((NameHoliday IS NOT NULL) OR (BelgianVacation IS NOT NULL), True, False),
Weekend         = IF( DATE_FORMAT( FullDateAlternateKey, "%W" ) IN ('Saturday','Sunday'), True, False);

-- ----------------------------------------------------------------------------------------------------------
-- Maak DimFlight
CREATE TABLE FlightDWH.DimFlight (
  FlightID INT NOT NULL PRIMARY KEY,
  FlightNumber VARCHAR(50),
  TotalNumberOfSeats SMALLINT,
  numberOfStops SMALLINT,
  ConnectingFlights VARCHAR(255)
);

-- dimflight vullen

-- Connectingflights momenteel nog null, data hebben we wss niet 

INSERT INTO flightdwh.dimflight (FlightID, FlightNumber, TotalNumberOfSeats, numberOfStops)
SELECT vd.flight_id, fd.flight_number, IFNULL(fa.total_seats, -1) as total_seats, fd.number_of_stops
FROM flight_oltp.flight_var_data vd 
JOIN flight_oltp.flight_fixed_data fd ON vd.flight_key = fd.flight_key
LEFT JOIN flight_oltp.flight_airplane fa ON fa.flight_number = fd.flight_number
WHERE NOT EXISTS (
  SELECT 1 FROM flightdwh.dimflight df WHERE df.FlightID = vd.flight_id
)
ORDER BY vd.flight_id;
-- ----------------------------------------------------------------------------------------------------------
-- Maak Fact Table met foreign keys
CREATE TABLE FlightDWH.FactFlight (
  FlightKey VARCHAR(50),
  AirlineKey VARCHAR(3),
  DepartDateKey DATE,
  ArrivalDateKey DATE,
  ScrapeDateKey DATE,
  FlightID INT,
  DepartAirportKey VARCHAR(20),
  ArrivalAirportKey VARCHAR(20),
  TicketPrice DECIMAL(10,2),
  NumberOfSeatsAvailable INT,
  DepartureTime TIME,
  ArrivalTime TIME,
  FOREIGN KEY (AirlineKey) REFERENCES DimAirline(AirlineCode),
  FOREIGN KEY (DepartDateKey) REFERENCES DimDate(DateKey),
  FOREIGN KEY (ArrivalDateKey) REFERENCES DimDate(DateKey),
  FOREIGN KEY (FlightID) REFERENCES DimFlight(FlightID),
  FOREIGN KEY (DepartAirportKey) REFERENCES DimAirport(AirportCode),
  FOREIGN KEY (ArrivalAirportKey) REFERENCES DimAirport(AirportCode),
  FOREIGN KEY (ScrapeDateKey) REFERENCES DimDate(DateKey)
);

INSERT INTO FlightDWH.FactFlight (
	FlightKey,
    AirlineKey,
    DepartDateKey,
    ArrivalDateKey,
    ScrapeDateKey,
    FlightID,
    DepartAirportKey,
    ArrivalAirportKey,
    TicketPrice,
    NumberOfSeatsAvailable,
    DepartureTime,
    ArrivalTime
)

-- Fill fact flight
SELECT
	CONCAT(vd.flight_key,'-',vd.flight_id) AS FlightKey,
    -- CONCAT(fa.iata, '-', fd.departure_date) AS AirlineKey,
    fa.iata AS AirlineKey,
    fd.departure_date AS DepartDateKey,
    fd.arrival_date AS ArrivalDateKey,
    vd.scrape_date AS ScrapeDateKey,
    vd.flight_id AS FlightID,
    da.iata AS DepartAirportKey,
    aa.iata AS ArrivalAirportKey,
    vd.price AS TicketPrice,
    vd.seats_available AS NumberOfSeatsAvailable,
    fd.departure_time AS DepartureTime,
    fd.arrival_time AS ArrivalTime
FROM 
    flight_oltp.flight_var_data vd 
    JOIN flight_oltp.flight_fixed_data fd ON vd.flight_key = fd.flight_key 
    JOIN flight_oltp.flight_airline fa ON fd.operating_airline = fa.iata 
    JOIN flight_oltp.flight_airport da ON fd.departure_airport = da.iata 
    JOIN flight_oltp.flight_airport aa ON fd.arrival_airport = aa.iata
ORDER BY DepartDateKey;

-- tijdelijke tabellen laten vallen
DROP TABLE IF EXISTS flightdwh.numbers_small;
DROP TABLE IF EXISTS flightdwh.numbers;
SET FOREIGN_KEY_CHECKS = 1;