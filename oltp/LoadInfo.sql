# 1) Algemeen
USE `flight_oltp` ; 
SET FOREIGN_KEY_CHECKS = 0; 
SET GLOBAL local_infile = 'ON';	# https://dba.stackexchange.com/questions/48751/enabling-load-data-local-infile-in-mysql

# 2) Tabel aanmaken
## Airplane
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_airplane`(
    type VARCHAR(30),
    age INT,
    total_seats INT,
    flight_number VARCHAR(10) NOT NULL,
    PRIMARY KEY (`type`),
    FOREIGN KEY (`flight_number`) REFERENCES `flight_oltp`.`flight_fixed_data` (`flight_number`)
);

# 3) Data inladen
## Airplane
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\LoadInfo.sql'
IGNORE INTO TABLE `flight_oltp`.`flight_airplane`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_number, @airplane_type  @airplane_age  @total_seats @distance_flown)
SET flight_number=@flight_number, type=@airplane_type, age=@airplane_age, total_seats=@total_seats;

## Airport
LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\LoadInfo.sql'
IGNORE INTO TABLE `flight_oltp`.`flight_airplane`
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(@flight_number, @airplane_type  @airplane_age  @total_seats @distance_flown)
SET distance_flown=@distance_flown;

## Alle instellingen terug op standaardinstellingen plaatsen.
SET FOREIGN_KEY_CHECKS = 1;
SET GLOBAL local_infile = 'OFF';

