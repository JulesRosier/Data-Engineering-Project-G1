-- flight_airport
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

-- flight_airline  
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