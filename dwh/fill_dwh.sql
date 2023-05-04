USE FlightDWH; 
SET SQL_SAFE_UPDATES = 0;
SET FOREIGN_KEY_CHECKS = 0;

-- DimAirport
-- Update reeds bestaande records
UPDATE FlightDWH.DimAirport dima SET 
AirportCode = (SELECT iata FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode),
AirportName = (SELECT name FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode),
City = (SELECT city FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode),
Country = (SELECT country FROM flight_oltp.flight_airport flighta WHERE flighta.iata = dima.AirportCode);

-- DimAirline
-- Insert nieuwe records
INSERT INTO FlightDWH.DimAirport (AirportCode, AirportName, City, Country)
SELECT DISTINCT iata, name, city, country
FROM flight_oltp.flight_airport
WHERE iata NOT IN (SELECT DISTINCT AirportCode FROM FlightDWH.DimAirport);

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

-- DimFlight
INSERT IGNORE FlightDWH.DimFlight (FlightKey, FlightNumber, TotalNumberOfSeats, numberOfStops, DepartureTime, ArrivalTime, Duration)
SELECT fd.flight_key, fd.flight_number, IFNULL(fa.total_seats, -1) as total_seats, fd.number_of_stops, fd.departure_time, fd.arrival_time, fd.duration
FROM flight_oltp.flight_fixed_data fd
LEFT JOIN flight_oltp.flight_airplane fa ON fa.flight_number = fd.flight_number
WHERE NOT EXISTS
(SELECT 1 FROM FlightDWH.DimFlight fdw WHERE fdw.FlightKey = fd.flight_key);

DROP TABLE IF EXISTS FlightDWH.DimFlightTemp;
CREATE TABLE FlightDWH.DimFlightTemp (
    id int NOT NULL,
    oltp_key VARCHAR(40),
    PRIMARY KEY (id)
);

INSERT INTO FlightDWH.DimFlightTemp (id, oltp_key)
SELECT df.id, fd.flight_key
FROM flight_oltp.flight_fixed_data fd
JOIN FlightDWH.DimFlight df on df.FlightKey = fd.flight_key
WHERE EXISTS
(SELECT 1 FROM FlightDWH.DimFlight fdw WHERE fdw.FlightKey = fd.flight_key)
AND (
 df.Duration <> fd.duration OR
 df.ArrivalTime <> fd.arrival_time OR
 df.DepartureTime <> fd.departure_time OR
 df.numberOfStops <> fd.number_of_stops
) and df.IsActive = 1;

UPDATE FlightDWH.DimFlight SET
EndDate = CURRENT_TIMESTAMP - second(1),
IsActive = false
WHERE EXISTS (select 1 from FlightDWH.DimFlightTemp t WHERE FlightDWH.DimFlight.id = t.id);

INSERT IGNORE FlightDWH.DimFlight (FlightKey, FlightNumber, TotalNumberOfSeats, numberOfStops, DepartureTime, ArrivalTime, Duration)
select fd.flight_key, fd.flight_number, IFNULL(fa.total_seats, -1) as total_seats, fd.number_of_stops, fd.departure_time, fd.arrival_time, fd.duration
from FlightDWH.DimFlightTemp t
JOIN flight_oltp.flight_fixed_data fd ON fd.flight_key = t.oltp_key
LEFT JOIN flight_oltp.flight_airplane fa ON fa.flight_number = fd.flight_number;

-- select * from FlightDWH.DimFlightTemp;
-- select * from FlightDWH.DimFlight where IsActive = false;

DROP TABLE IF EXISTS FlightDWH.DimFlightTemp;

-- FachtFlight
INSERT IGNORE INTO FlightDWH.FactFlight (
	FlightKey,
    AirlineKey,
    DepartDateKey,
    ArrivalDateKey,
    ScrapeDateKey,
    FlightID,
    DepartAirportKey,
    ArrivalAirportKey,
    TicketPrice,
    NumberOfSeatsAvailable
)

-- Fill fact flight
SELECT
	vd.flight_key AS FlightKey,
    (SELECT AirlineKey FROM FlightDWH.DimAirline WHERE AirlineCode = fa.iata) AS AirlineKey,
    UNIX_TIMESTAMP(fd.departure_date) AS DepartDateKey,
    UNIX_TIMESTAMP(fd.arrival_date) AS ArrivalDateKey,
    UNIX_TIMESTAMP(vd.scrape_date) AS ScrapeDateKey,
    df.id AS FlightID,
    (SELECT AirportKey FROM FlightDWH.DimAirport WHERE AirportCode = da.iata) AS DepartAirportKey,
    (SELECT AirportKey FROM FlightDWH.DimAirport WHERE AirportCode = aa.iata) AS ArrivalAirportKey,
    vd.price AS TicketPrice,
    vd.seats_available AS NumberOfSeatsAvailable
FROM 
    flight_oltp.flight_var_data vd 
    JOIN flight_oltp.flight_fixed_data fd ON vd.flight_key = fd.flight_key 
    JOIN flight_oltp.flight_airline fa ON fd.operating_airline = fa.iata 
    JOIN flight_oltp.flight_airport da ON fd.departure_airport = da.iata 
    JOIN flight_oltp.flight_airport aa ON fd.arrival_airport = aa.iata
    JOIN FlightDWH.DimFlight df ON fd.flight_key = df.FlightKey
    WHERE df.IsActive = 1;
ORDER BY DepartDateKey;

SET FOREIGN_KEY_CHECKS = 1;