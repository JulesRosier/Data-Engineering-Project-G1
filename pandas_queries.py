import pandas as pd

flights = pd.read_csv('queries.csv')

only_ryanair = (flights['name'] == 'Ryanair')
only_tui = (flights['name'] == 'TuiFly')
only_brussels = (flights['airport_code_depart_id'] == 'BRU')
only_charleroi = (flights['airport_code_depart_id'] == 'CRL')

# Ryanair	Brussel-Zaventem	Malaga	Aantal vluchten	    April
ryanair_flights = flights[only_ryanair & only_brussels &(flights['airport_code_arrival_id'] == 'AGP')]
april_flights = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-04')]
print(len(april_flights))

# Ryanair	Brussel-Zaventem	Palma	Gemiddelde prijs	Mei
ryanair_flights = flights[only_ryanair & only_brussels & (flights['airport_code_arrival_id'] == 'PMI')]
may_flights = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-05')]
average_price = may_flights['ticket_price'].mean()
print(average_price)

# Ryanair	Brussel-Zaventem	Malaga     Totaal aantal plaatsen beschikbaar	Juni
ryanair_flights = flights[only_ryanair & only_brussels & (flights['airport_code_arrival_id'] == 'AGP')]
june_flights = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-06')]
seats_number = june_flights['number_seats_available'].sum()
print(seats_number)

# Ryanair	Brussel-Zaventem	Tenerife	Aantal vluchten	01/09 tot en met 14/09
ryanair_flights = flights[only_ryanair & only_brussels & (flights['airport_code_arrival_id'] == 'TFS')]
start_date = '2023-05-01'
end_date = '2023-09-14'
september_flights = ryanair_flights[(ryanair_flights['datetime_depart'] >= start_date) & (ryanair_flights['datetime_depart'] <= end_date)]
total = len(september_flights)
print(total)

# Ryanair	Charleroi	Alicante	Aantal vluchten	Juni
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'ALC')]
june_flights = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-06')]
print(len(june_flights))

# Ryanair	Charleroi	Ibiza	Aantal vluchten	15/08 tot en met 27/08
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'IBZ')]
start_date = '2023-08-15'
end_date = '2023-08-27'
august_flights = ryanair_flights[(ryanair_flights['datetime_depart'] >= start_date) & (ryanair_flights['datetime_depart'] <= end_date)]
total = len(august_flights)
print(total)

# Ryanair	Charleroi	Malaga	Vertrekuur	8-apr
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'AGP')]
flight = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-04-08')]
depart = flight['datetime_depart']
print(depart)

# Ryanair	Charleroi	Palma	Aankomstuur	19-apr
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'PMI')]
flight = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-04-19')]
arrival = flight['datetime_arrival']
print(arrival)

# Ryanair	Charleroi	Tenerife	Gemiddelde prijs	15-mei
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'TFS')]
may_flights = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-05-15')]
average_price = may_flights['ticket_price'].mean()
print(average_price)

# Ryanair	Charleroi	Napels	Aantal plaatsen beschikbaar	19-apr
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'NAP')]
flight = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-04-19')]
seats = flight['number_seats_available']
print(seats)

# Ryanair	Charleroi	Palermo	Aantal tussenstops	26-mei
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'PMO')]
flight = ryanair_flights[ryanair_flights['datetime_depart'].str.contains('2023-05-26')]
stops = flight['number_of_stops']
print(stops)

# Ryanair	Charleroi	Brindisi	Gemiddelde prijs	15/09 tot en met 30/10
ryanair_flights = flights[only_ryanair & only_charleroi & (flights['airport_code_arrival_id'] == 'BDS')]
start_date = '2023-09-15'
end_date = '2023-10-30'
sep_oct_flights = ryanair_flights[(ryanair_flights['datetime_depart'] >= start_date) & (ryanair_flights['datetime_depart'] <= end_date)]
average_price = sep_oct_flights['ticket_price'].mean()
print(average_price)

# TUI	Brugge - Oostende	Brindisi	Aantal vluchten	Augustus
tui_flights = flights[only_tui & (flights['airport_code_depart_id'] == 'OST') & (flights['airport_code_arrival_id'] == 'BDS')]
august_flights = tui_flights[tui_flights['datetime_depart'].str.contains('2023-08')]
print(len(august_flights))

# TUI	Antwerpen	Alicante	Gemiddelde prijs	Juni
tui_flights = flights[only_tui & (flights['airport_code_depart_id'] == 'ANR') & (flights['airport_code_arrival_id'] == 'ALC')]
june_flights = tui_flights[tui_flights['datetime_depart'].str.contains('2023-06')]
average_price = june_flights['ticket_price'].mean()
print(average_price)

# TUI	Luik	Rhodos	Gemiddelde prijs	April
tui_flights = flights[only_tui & (flights['airport_code_depart_id'] == 'LGG') & (flights['airport_code_arrival_id'] == 'RHO')]
april_flights = tui_flights[tui_flights['datetime_depart'].str.contains('2023-04')]
average_price = april_flights['ticket_price'].mean()
print(average_price)

# TUI	Brussel	Brindisi	Vertrekuur	18-jul
tui_flights = flights[only_tui & (flights['airport_code_depart_id'] == 'BRU') & (flights['airport_code_arrival_id'] == 'BDS')]
flight = tui_flights[tui_flights['datetime_depart'].str.contains('2023-07-18')]
depart = flight['datetime_depart'].unique()
print(depart)

# TUI	Luik	Alicante	Aankomstuur	19-jun
tui_flights = flights[only_tui & (flights['airport_code_depart_id'] == 'LGG') & (flights['airport_code_arrival_id'] == 'ALC')]
flight = tui_flights[tui_flights['datetime_depart'].str.contains('2023-06-19')]
arrival = flight['datetime_arrival'].unique()
print(arrival)

# TUI	Brussel	Corfu	Aantal tussenstops	23-mei
tui_flights = flights[only_tui & (flights['airport_code_depart_id'] == 'BRU') & (flights['airport_code_arrival_id'] == 'CFU')]
flight = tui_flights[tui_flights['datetime_depart'].str.contains('2023-05-23')]
stops = flight['number_of_stops'].unique()
print(stops)

# TUI	Brugge - Oostende	Rhodos	Aantal plaatsen beschikbaar	30-mei
tui_flights = flights[only_ryanair & (flights['airport_code_depart_id'] == 'OST') & (flights['airport_code_arrival_id'] == 'RHO')]
flight = tui_flights[tui_flights['datetime_depart'].str.contains('2023-05-30')]
seats = flight['number_seats_available']
print(seats)

# Brussels Airlines	Brussel	Alicante	Aantal vluchten	Mei
# Brussels Airlines	Brussel	Ibiza	Gemiddelde prijs	Juni
# Brussels Airlines	Brussel	Tenerife	Aantal vluchten	13-mei
# Brussels Airlines	Brussel	Rhodos	Totaal aantal vluchten	06/06 - 07/07
# Brussels Airlines	Brussel	Brindisi	Vertrekuur	Mei
# Brussels Airlines	Brussel	Napels	Aankomstuur	Juni
# Brussels Airlines	Brussel	Palermo	Aantal tussenstops	Juli
# Brussels Airlines	Brussel	Faro	Gemiddelde prijs	April
# Brussels Airlines	Brussel	Alicante	Aantal vluchten	Juli
# Brussels Airlines	Brussel	Ibiza	Vertrekuur	Juni
# Brussels Airlines	Brussel	Malaga	Aankomstuur	Juli
# Brussels Airlines	Brussel	Tenerife	Aantal tussenstops	April