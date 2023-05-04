DROP DATABASE IF EXISTS FlightDWH;
CREATE DATABASE FlightDWH;
USE FlightDWH; 
SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------------------------------------
-- Maak DimAirport
CREATE TABLE IF NOT EXISTS FlightDWH.DimAirport(
	AirportKey INT AUTO_INCREMENT PRIMARY KEY,
    AirportCode CHAR(3) UNIQUE NOT NULL,
    AirportName VARCHAR(50),
    City VARCHAR(50),
    Country VARCHAR(50)
);

-- ----------------------------------------------------------------------------------------------------------
-- Maak DimAirline
CREATE TABLE IF NOT EXISTS FlightDWH.DimAirline (
	AirlineKey INT AUTO_INCREMENT PRIMARY KEY,
	AirlineCode CHAR(3) UNIQUE NOT NULL,
	AirlineName VARCHAR(50),
	AirlineContact VARCHAR(50),
	AirlineAddress VARCHAR(100)
);


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
  DateKey INT,
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
SELECT UNIX_TIMESTAMP(date_add('2023-01-01', INTERVAL number DAY)), date_add('2023-01-01', INTERVAL number DAY)
FROM numbers
WHERE DATE_ADD( '2023-01-01', INTERVAL number DAY ) BETWEEN '2023-01-01' AND '2023-12-31'
ORDER BY number;

DROP TABLE IF EXISTS FlightDWH.numbers_small;
CREATE TABLE FlightDWH.numbers_small (number INT);
INSERT INTO FlightDWH.numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

DROP TABLE IF EXISTS FlightDWH.numbers;
CREATE TABLE FlightDWH.numbers (number BIGINT);
INSERT INTO FlightDWH.numbers
SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number
FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones
LIMIT 1000000;

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
  id int NOT NULL AUTO_INCREMENT,
  FlightKey VARCHAR(40) NOT NULL,
  FlightNumber VARCHAR(50),
  TotalNumberOfSeats SMALLINT,
  numberOfStops SMALLINT,
  DepartureTime TIME,
  ArrivalTime TIME,
  Duration TIME,
  ConnectingFlights VARCHAR(255),
  StartDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  EndDate DATETIME DEFAULT '9999-12-31 23:59:59',
  IsActive BOOLEAN DEFAULT true,
  PRIMARY KEY (id)
);

CREATE TABLE FlightDWH.FactFlight (
  FlightKey VARCHAR(50),
  AirlineKey INT,
  DepartDateKey INT,
  ArrivalDateKey INT,
  ScrapeDateKey INT,
  FlightID INT,
  DepartAirportKey INT,
  ArrivalAirportKey INT,
  TicketPrice DECIMAL(10,2),
  NumberOfSeatsAvailable INT,
  FOREIGN KEY (AirlineKey) REFERENCES DimAirline(AirlineKey),
  FOREIGN KEY (DepartDateKey) REFERENCES DimDate(DateKey),
  FOREIGN KEY (ArrivalDateKey) REFERENCES DimDate(DateKey),
  FOREIGN KEY (DepartAirportKey) REFERENCES DimAirport(AirportKey),
  FOREIGN KEY (ArrivalAirportKey) REFERENCES DimAirport(AirportKey),
  FOREIGN KEY (ScrapeDateKey) REFERENCES DimDate(DateKey),
  FOREIGN KEY (FlightID) REFERENCES DimFlight(id)
);


DROP TABLE IF EXISTS flightdwh.numbers_small;
DROP TABLE IF EXISTS flightdwh.numbers;
SET FOREIGN_KEY_CHECKS = 1;