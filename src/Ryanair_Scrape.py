from bs4 import BeautifulSoup
from datetime import datetime, time
from decimal import Decimal
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
                    try:
                        flight_data = flight['dates'][0]['flights'][0]

                        if Flight.select().where(Flight.flight_key == flight_data['flightKey']).exists():
                            flight_obj = Flight.get(flight_key = flight_data['flightKey'])
                            bestaal_all = True
                        else:
                            flight_obj = Flight(flight_key = flight_data['flightKey'])
                            bestaal_all = False

                        flight_obj.last_updated           = datetime.now()
                        flight_obj.airline_id             = 1
                        flight_obj.airport_code_depart    = flight['origin']
                        flight_obj.airport_code_arrival   = flight['destination']
                        flight_obj.airport_depart         = flight['originName']
                        flight_obj.airport_arrival        = flight['destinationName']
                        flight_obj.datetime_depart        = datetime.fromisoformat(flight_data['time'][0])
                        flight_obj.datetime_arrival       = datetime.fromisoformat(flight_data['time'][1])
                        flight_obj.flight_duration        = time.fromisoformat(flight_data['duration']+':00')
                        flight_obj.ticket_price           = Decimal(flight_data['regularFare']['fares'][0]['amount'])
                        flight_obj.number_seats_total     = None
                        flight_obj.number_seats_available = int(flight_data['faresLeft'])
                        flight_obj.number_of_stops        = len(flight_data['segments']) - 1
                        flight_obj.connection_flight      = len(flight_data['segments']) == 0
                        flight_obj.flight_number          = flight_data['flightNumber']

                        if bestaal_all:
                            flight_obj.save()
                        else:
                            flight_obj.save(force_insert=True)

                    except Exception as e: print(e)

    return (flights)
