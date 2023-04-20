# Airport
INSERT INTO `flight_oltp`.`flight_airport` (`iata`, `name`, `city`, `country`)
VALUES 
('CRL', 'Brussels South Charleroi Airport', 'Charleroi', 'Belgium'),
('BRU', 'Brussels Airport', 'Brussels', 'Belgium'),
('ANR', 'Antwerp International Airport', 'Antwerp', 'Belgium'),
('LGG', 'Liège Airport', 'Liège', 'Belgium'),
('OST', 'Ostend–Bruges International Airport', 'Ostend', 'Belgium'),
('CFU', 'Corfu International Airport', 'Corfu', 'Greece'),
('BDS', 'Brindisi Airport', 'Brindisi', 'Italy'),
('NAP', 'Naples International Airport', 'Naples', 'Italy'),
('ALC', 'Alicante–Elche Airport', 'Alicante', 'Spain'),
('RHO', 'Rhodes International Airport', 'Rhodes', 'Greece'),
('AGP', 'Málaga Airport', 'Málaga', 'Spain'),
('PMI', 'Palma de Mallorca Airport', 'Palma de Mallorca', 'Spain'),
('HER', 'Heraklion International Airport', 'Heraklion', 'Greece'),
('PMO', 'Falcone–Borsellino Airport', 'Palermo', 'Italy'),
('FAO', 'Faro Airport', 'Faro', 'Portugal'),
('TFS', 'Tenerife South Airport', 'Tenerife', 'Spain'),
('IBZ', 'Ibiza Airport', 'Ibiza', 'Spain');

# Airline
INSERT INTO `flight_oltp`.`flight_airline` (`iata`, `name`) VALUES
('FR', 'Ryanair'),
('HV', 'Transavia'),
('TB', 'TUI fly'),
('SN', 'Brussels Airlines');