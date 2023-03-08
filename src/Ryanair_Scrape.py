from bs4 import BeautifulSoup
from datetime import datetime, time
import decimal
import requests
import json
from repository import Flight

from pprint import pprint

# CONSTS
DEPART = ['BRU', 'CRL']
# ROUND_TRIP = 'false'
# INCLUDE_CONNECTING_FLIGHTS = 'false'
URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn={date}&DateOut={date}&Destination={place}&Disc=0&INF=0&Origin={origin}&IncludeConnectingFlights=false&RoundTrip=false&ToUs=AGREED"


def get_data(arive, dates) -> dict:
    # Flight.create(flight_key='aaaaaaaaa')
    flights = []
    for place in arive:
        for origin in DEPART:
            for date in dates:
                print(f"Pulling {origin} to {place} on {date}")
                page = requests.get(URL.format(
                    date=date, place=place, origin=origin))
                soup = BeautifulSoup(page.content, "lxml")
                result = soup.find("p").text
                json_reponse = json.loads(result)

                for flight in json_reponse['trips']:
                    if flight['dates'][0]['flights'] == []:
                        break
                    out = {}
                    try:
                        out['depart'] = flight['origin']
                        out['departLocation'] = flight['originName']
                        out['destination'] = flight['destination']
                        out['destinationLocation'] = flight['destinationName']
                        flight_data = flight['dates'][0]['flights'][0]
                        out['departure_time'] = datetime.fromisoformat(
                            flight_data['time'][0]).strftime("%Y-%m-%d %H:%M:%S")
                        out['arrival_time'] = datetime.fromisoformat(
                            flight_data['time'][1]).strftime("%Y-%m-%d %H:%M:%S")
                        out['duration'] = flight_data['duration']
                        out['flightKey'] = flight_data['flightKey']
                        out['flightNumber'] = flight_data['flightNumber']
                        out['price'] = flight_data['regularFare']['fares'][0]['amount']
                        out['faresLeft'] = flight_data['faresLeft']
                        # aantal stops - segments tellen?
                        
                        Flight.create(airline_name        = 'Ryanair',
                                   airport_code_depart    = flight['origin'],
                                   airport_code_arrival   = flight['destination'],
                                   datetime_depart        = datetime.fromisoformat(flight_data['time'][0]),
                                   datetime_arrival       = datetime.fromisoformat(flight_data['time'][1]),
                                   flight_duration        = time.fromisoformat(flight_data['duration']+':00'),
                                   ticket_price           = decimal.Decimal(flight_data['regularFare']['fares'][0]['amount']),
                                   number_seats_total     = 0,
                                   number_seats_available = int(flight_data['faresLeft']),
                                   number_of_stops        = 0,
                                   flight_key             = flight_data['flightKey'],
                                   flight_number          = flight_data['flightNumber']
                                )
                        flights.append(out)
                    except Exception as ex:
                        print('iets ging mis')

    return (flights)
