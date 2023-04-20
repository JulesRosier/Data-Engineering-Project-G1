# 1) Tabel aanmaken
## Airplane
CREATE TABLE IF NOT EXISTS `flight_oltp`.`flight_airplane`(
    type VARCHAR(30),
    age INT,
    total_seats INT,
    flight_number VARCHAR(10) NOT NULL,
    PRIMARY KEY (`type`),
    FOREIGN KEY (`flight_number`) REFERENCES `flight_oltp`.`flight_fixed_data` (`flight_number`)
);

# 2) Data inladen
## Airplane