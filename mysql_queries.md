# Handige Queries

## Join de het flight met de meest recenste data (old)

```sql
select f.*, d1.datetime_scraped, d1.number_seats_available, d1.ticket_price, d1.datetime_depart, d1.datetime_arrival
from flights f
join flight_data d1 on d1.flight_key_id = f.flight_key
left outer join flight_data d2 on (f.flight_key = d2.flight_key_id and
	(d1.datetime_scraped < d2.datetime_scraped or (d1.datetime_scraped = d2.datetime_scraped and d1.datetime_scraped < d2.datetime_scraped)))
where d2.flight_key_id is null;
```

# Maak de lokale OLTP databank aan voor de CSV-bestanden

```sql
# 1) Databank aanmaken
CREATE SCHEMA IF NOT EXISTS `flight_oltp` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `flight_oltp` ;
SET FOREIGN_KEY_CHECKS = 0;

# 2) Tabellen aanmaken
# Flight Fixed Data
DROP TABLE IF EXISTS `flight_oltp`.`flight_fixed_data`;
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_fixed_data` (
  flight_key VARCHAR(40) NOT NULL,
  fligh_number VARCHAR(10),
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
DROP TABLE IF EXISTS `flight_oltp`.`flight_var_data`;
CREATE TABLE `flight_oltp`.`flight_var_data` (
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
  FOREIGN KEY (`flight_key`)
    REFERENCES `flight_oltp`.`flight_fixed_data` (`flight_key`)
);

# Airport
DROP TABLE IF EXISTS `flight_oltp`.`flight_airport`;
CREATE TABLE `flight_oltp`.`flight_airport`(
    iata VARCHAR(5) NOT NULL,
    PRIMARY KEY (`iata`)
);

# Airline
DROP TABLE IF EXISTS `flight_oltp`.`flight_airline`;
CREATE TABLE `flight_oltp`.`flight_airline`(
    iata VARCHAR(5) NOT NULL,
    PRIMARY KEY (`iata`)
);
```
