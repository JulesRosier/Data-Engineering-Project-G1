-- LoadFiles --
-- 1) Algemeen
DROP DATABASE IF EXISTS flight_oltp;
CREATE DATABASE flight_oltp;
USE flight_oltp; 
SET GLOBAL local_infile = "ON";
SET FOREIGN_KEY_CHECKS = 0;

-- 2) Tabellen aanmaken
-- Airport
CREATE TABLE IF NOT EXISTS flight_oltp.flight_airport(
    iata CHAR(3) UNIQUE NOT NULL,
    name VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100),
    PRIMARY KEY (iata)
);

-- Flight Airport Distance
CREATE TABLE IF NOT EXISTS flight_oltp.flight_airport_distance(
    airport1_iata CHAR(3) NOT NULL,
    airport2_iata CHAR(3) NOT NULL,
    distance_flown INT,
    PRIMARY KEY (airport1_iata, airport2_iata),
    FOREIGN KEY (airport1_iata) REFERENCES flight_oltp.flight_airport (iata),
    FOREIGN KEY (airport2_iata) REFERENCES flight_oltp.flight_airport (iata)
);

-- Airline
CREATE TABLE IF NOT EXISTS flight_oltp.flight_airline(
    iata CHAR(3) UNIQUE NOT NULL,
    name VARCHAR(100),
    PRIMARY KEY (iata)
);

-- Flight Fixed Data
CREATE TABLE IF NOT EXISTS flight_oltp.flight_fixed_data (
  flight_key VARCHAR(40) NOT NULL,
  flight_number VARCHAR(10),
  number_of_stops INT,
  departure_date DATE,
  arrival_date DATE,
  departure_time TIME,
  arrival_time TIME,
  duration TIME,
  departure_airport VARCHAR(5) NOT NULL,
  arrival_airport VARCHAR(5) NOT NULL,
  operating_airline VARCHAR(5) NOT NULL,
  PRIMARY KEY (flight_key),
  FOREIGN KEY (departure_airport) REFERENCES flight_oltp.flight_airport (iata),
  FOREIGN KEY (arrival_airport) REFERENCES flight_oltp.flight_airport (iata),
  FOREIGN KEY (operating_airline) REFERENCES flight_oltp.flight_airline (iata)
  );

  CREATE INDEX idx_flight_nr ON flight_fixed_data(flight_number);

-- Flight Var Data
CREATE TABLE IF NOT EXISTS flight_oltp.flight_var_data (
  flight_id INT NOT NULL auto_increment,
  scrape_date DATE,
  price DECIMAL(4, 2),
  seats_available INT,
  flight_key VARCHAR(40) NOT NULL,
  PRIMARY KEY (flight_id),
  FOREIGN KEY (flight_key) REFERENCES flight_oltp.flight_fixed_data (flight_key)
);

  -- Airplane
CREATE TABLE IF NOT EXISTS flight_oltp.flight_airplane(
    airplane_type VARCHAR(30),
    airplane_age INT,
    total_seats INT,
    flight_number VARCHAR(10) NOT NULL,
    PRIMARY KEY (airplane_type),
    FOREIGN KEY (flight_number) REFERENCES flight_oltp.flight_fixed_data (flight_number)
);

-- 3) Data inladen
-- Airport 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
IGNORE INTO TABLE `flight_oltp`.`flight_airport`
CHARACTER SET UTF8
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET iata = @departure_airport_iata_code;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
IGNORE INTO TABLE `flight_oltp`.`flight_airport`
CHARACTER SET UTF8
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET iata = @arrival_airport_iata_code;


-- Airline 
LOAD DATA INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv"
IGNORE INTO TABLE flight_oltp.flight_airline
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\n"
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET iata=@airline_iata_code;

-- Fixed Flight_Data 
LOAD DATA INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv"
IGNORE INTO TABLE flight_oltp.flight_fixed_data
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\n"
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET flight_key=@flight_id, flight_number=@flight_number, number_of_stops=@number_of_stops, departure_date=@departure_date, arrival_date=@arrival_date, departure_time=@departure_time, arrival_time=@arrival_time, duration=@duration, departure_airport=@departure_airport_iata_code, arrival_airport=@arrival_airport_iata_code, operating_airline=@airline_iata_code;

-- Var Flight_Data 
LOAD DATA INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv"
IGNORE INTO TABLE flight_oltp.flight_var_data
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\n"
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET scrape_date=@scrape_date, price=@price, seats_available=@available_seats, flight_key=@flight_id;

-- Airplane
LOAD DATA INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\LoadInfo.csv"
IGNORE INTO TABLE flight_oltp.flight_airplane
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\n"
(@flight_number, @airplane_type, @airplane_age, @total_seats, @distance_flown)
SET flight_number=@flight_number, airplane_type=@airplane_type, airplane_age=@airplane_age, total_seats=@total_seats;

-- Alle instellingen terug op standaardinstellingen plaatsen.
SET GLOBAL local_infile = "OFF";
SET FOREIGN_KEY_CHECKS = 1;

-- Seeding
UPDATE flight_oltp.flight_airport
SET name = 'Brussels South Charleroi Airport', city = 'Charleroi', country = 'Belgium'
WHERE iata = 'CRL';

UPDATE flight_oltp.flight_airport
SET name = 'Brussels Airport', city = 'Brussels', country = 'Belgium'
WHERE iata = 'BRU';

UPDATE flight_oltp.flight_airport
SET name = 'Antwerp International Airport', city = 'Antwerp', country = 'Belgium'
WHERE iata = 'ANR';

UPDATE flight_oltp.flight_airport
SET name = 'Liege Airport', city = 'Liege', country = 'Belgium'
WHERE iata = 'LGG';

UPDATE flight_oltp.flight_airport
SET name = 'Ostend Bruges International Airport', city = 'Ostend', country = 'Belgium'
WHERE iata = 'OST';

UPDATE flight_oltp.flight_airport
SET name = 'Corfu International Airport', city = 'Corfu', country = 'Greece'
WHERE iata = 'CFU';

UPDATE flight_oltp.flight_airport
SET name = 'Brindisi Airport', city = 'Brindisi', country = 'Italy'
WHERE iata = 'BDS';

UPDATE flight_oltp.flight_airport
SET name = 'Naples International Airport', city = 'Naples', country = 'Italy'
WHERE iata = 'NAP';

UPDATE flight_oltp.flight_airport
SET name = 'Alicante Elche Airport', city = 'Alicante', country = 'Spain'
WHERE iata = 'ALC';

UPDATE flight_oltp.flight_airport
SET name = 'Rhodes International Airport', city = 'Rhodes', country = 'Greece'
WHERE iata = 'RHO';

UPDATE flight_oltp.flight_airport
SET name = 'Malaga Airport', city = 'Malaga', country = 'Spain'
WHERE iata = 'AGP';

UPDATE flight_oltp.flight_airport
SET name = 'Palma de Mallorca Airport', city = 'Palma de Mallorca', country = 'Spain'
WHERE iata = 'PMI';

UPDATE flight_oltp.flight_airport
SET name = 'Heraklion International Airport', city = 'Heraklion', country = 'Greece'
WHERE iata = 'HER';

UPDATE flight_oltp.flight_airport
SET name = 'Falcone Borsellino Airport', city = 'Palermo', country = 'Italy'
WHERE iata = 'PMO';

UPDATE flight_oltp.flight_airport
SET name = 'Faro Airport', city = 'Faro', country = 'Portugal'
WHERE iata = 'FAO';

UPDATE flight_oltp.flight_airport
SET name = 'Tenerife South Airport', city = 'Tenerife', country = 'Spain'
WHERE iata = 'TFS';

UPDATE flight_oltp.flight_airport
SET name = 'Ibiza Airport', city = 'Ibiza', country = 'Spain'
WHERE iata = 'IBZ';

UPDATE flight_oltp.flight_airline
SET name = 'Ryanair'
WHERE iata = 'FR';

UPDATE flight_oltp.flight_airline
SET name = 'Transavia'
WHERE iata = 'HV';

UPDATE flight_oltp.flight_airline
SET name = 'TUI fly'
WHERE iata = 'TB';

UPDATE flight_oltp.flight_airline
SET name = 'Brussels Airlines'
WHERE iata = 'SN';

-- Flight Airport Distance
LOAD DATA INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\LoadInfo.csv"
IGNORE INTO TABLE flight_oltp.flight_airport_distance
FIELDS TERMINATED BY ","
LINES TERMINATED BY "\n"
(@flight_number, @airplane_type, @airplane_age, @total_seats, @distance_flown)
SET distance_flown=@distance_flown,
airport1_iata=(select departure_airport from flight_fixed_data where flight_number = @flight_number LIMIT 1),
airport2_iata=(select arrival_airport from flight_fixed_data where flight_number = @flight_number LIMIT 1);