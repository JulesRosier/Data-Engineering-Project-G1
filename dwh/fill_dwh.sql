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
INSERT INTO FlightDWH.DimFlight (FlightKey, FlightNumber, TotalNumberOfSeats, numberOfStops, DepartureTime, ArrivalTime, Duration)
SELECT fd.flight_key, fd.flight_number, IFNULL(fa.total_seats, -1) as total_seats, fd.number_of_stops, fd.departure_date, fd.arrival_time, fd.duration
FROM flight_oltp.flight_fixed_data fd
LEFT JOIN flight_oltp.flight_airplane fa ON fa.flight_number = fd.flight_number
ON DUPLICATE KEY UPDATE
  FlightNumber = VALUES(FlightNumber),
  TotalNumberOfSeats = VALUES(TotalNumberOfSeats),
  numberOfStops = VALUES(numberOfStops),
  DepartureTime = VALUES(DepartureTime),
  ArrivalTime = VALUES(ArrivalTime),
  FlightDWH.DimFlight.Duration = VALUES(Duration),
  ConnectingFlights = VALUES(ConnectingFlights),
  IsActive = true,
  EndDate = CASE
              WHEN VALUES(FlightNumber) <> FlightNumber OR
                   VALUES(TotalNumberOfSeats) <> TotalNumberOfSeats OR
                   VALUES(numberOfStops) <> numberOfStops OR
                   VALUES(DepartureTime) <> DepartureTime OR
                   VALUES(ArrivalTime) <> ArrivalTime OR
                   VALUES(Duration) <> FlightDWH.DimFlight.Duration OR
                   VALUES(ConnectingFlights) <> ConnectingFlights
              THEN CURRENT_TIMESTAMP
              ELSE EndDate
            END;
-- FachtFlight

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
    NumberOfSeatsAvailable
)

-- Fill fact flight
SELECT
	vd.flight_key AS FlightKey,
    (SELECT AirlineKey FROM FlightDWH.DimAirline WHERE AirlineCode = fa.iata) AS AirlineKey,
    UNIX_TIMESTAMP(fd.departure_date) AS DepartDateKey,
    UNIX_TIMESTAMP(fd.arrival_date) AS ArrivalDateKey,
    UNIX_TIMESTAMP(vd.scrape_date) AS ScrapeDateKey,
    vd.flight_id AS FlightID,
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
ORDER BY DepartDateKey;

SET FOREIGN_KEY_CHECKS = 1;