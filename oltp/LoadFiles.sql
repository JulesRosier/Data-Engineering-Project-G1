# 1) Databank aanmaken
CREATE SCHEMA IF NOT EXISTS `flight_oltp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `flight_oltp` ; 
SET FOREIGN_KEY_CHECKS = 0; 
SET GLOBAL local_infile = 'ON';		# https://dba.stackexchange.com/questions/48751/enabling-load-data-local-infile-in-mysql

# 2) Tabellen aanmaken
## Airport
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_airport`(
    iata VARCHAR(5) UNIQUE NOT NULL,
    PRIMARY KEY (`iata`)
);

## Airline
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_airline`(
    iata VARCHAR(5) UNIQUE NOT NULL,
    PRIMARY KEY (`iata`)
);

## Flight Fixed Data
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_fixed_data` (
  flight_key VARCHAR(40) NOT NULL,
  flight_number VARCHAR(10),
  number_of_stops INT,
  departure_airport VARCHAR(5) NOT NULL,
  arrival_airport VARCHAR(5) NOT NULL,
  operating_airline VARCHAR(5) NOT NULL,
  PRIMARY KEY (`flight_key`),
  FOREIGN KEY (`departure_airport`) REFERENCES `flight_oltp`.`Flight_Airport` (`iata`),
  FOREIGN KEY (`arrival_airport`) REFERENCES `flight_oltp`.`Flight_Airport` (`iata`),
  FOREIGN KEY (`operating_airline`) REFERENCES `flight_oltp`.`Flight_Airline` (`iata`)
  );

# Flight Var Data
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_var_data` (
  flight_id INT NOT NULL auto_increment,
  flight_key VARCHAR(40) NOT NULL,
  scrape_date DATE,
  departure_date DATE,
  arrival_date DATE,
  departure_time TIME,
  arrival_time TIME,
  duration TIME,
  price DECIMAL(4, 2),
  seats_available INT,
  PRIMARY KEY (`flight_id`),
  FOREIGN KEY (`flight_key`) REFERENCES `flight_oltp`.`flight_fixed_data` (`flight_key`)
);

# 3) Data inladen
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'

## Airport 
IGNORE INTO TABLE `flight_oltp`.`flight_airport`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET iata=@departure_airport_iata_code, iata=@arrival_airport_iata_code;

## Airline 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
IGNORE INTO TABLE `flight_oltp`.`flight_airline`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET iata=@airline_iata_code;

# Fixed Flight_Data 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
IGNORE INTO TABLE `flight_oltp`.`flight_fixed_data`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET flight_key=@flight_id, flight_number=@flight_number, number_of_stops=@number_of_stops, departure_airport=@departure_airport_iata_code, arrival_airport=@arrival_airport_iata_code, operating_airline=@airline_iata_code;

#  Var Flight_Data 
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\All.csv'
IGNORE INTO TABLE `flight_oltp`.`flight_var_data`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_id, @flight_number, @departure_date, @arrival_date, @departure_time, @arrival_time, @duration, @number_of_stops, @airline_iata_code, @departure_airport_iata_code, @arrival_airport_iata_code, @scrape_date, @available_seats, @price)
SET flight_key=@flight_id, scrape_date=@scrape_date, departure_date=@departure_date, arrival_date=@arrival_date, departure_time=@departure_time, arrival_time=@arrival_time, duration=@duration, price=@price, seats_available=@available_seats;

# Alle instellingen terug op standaardinstellingen plaatsen.
SET FOREIGN_KEY_CHECKS = 1;
SET GLOBAL local_infile = 'OFF';