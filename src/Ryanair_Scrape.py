from bs4 import BeautifulSoup
from datetime import datetime, time
from decimal import Decimal
import requests
import json
from repository import Flight

from pprint import pprint

from repository import FlightData

# CONSTS
DEPART = ['BRU', 'CRL']
# ROUND_TRIP = 'false'
# INCLUDE_CONNECTING_FLIGHTS = 'false'
URL = "https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn={date}&DateOut={date}&Destination={place}&Disc=0&INF=0&Origin={origin}&IncludeConnectingFlights=false&RoundTrip=false&ToUs=AGREED"

def get_data(arive, dates) -> dict:
    for place in arive:
        for origin in DEPART:
            for date in dates:
                print(f"Pulling {origin} to {place} on {date}")
                page = requests.get(URL.format(
                    date=date, place=place, origin=origin), timeout=10)
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
                        else:
                            flight_obj = Flight(flight_key = flight_data['flightKey'])

                            flight_obj.airline_id             = 1
                            flight_obj.airport_code_depart    = flight['origin']
                            flight_obj.airport_code_arrival   = flight['destination']
                            flight_obj.flight_duration        = time.fromisoformat(flight_data['duration']+':00')
                            flight_obj.number_seats_total     = None
                            flight_obj.number_of_stops        = len(flight_data['segments']) - 1
                            flight_obj.connection_flight      = len(flight_data['segments']) == 0
                            flight_obj.flight_number          = flight_data['flightNumber']

                            flight_obj.save(force_insert=True)

                        flight_data_obj = FlightData()

                        flight_data_obj.datetime_depart        = datetime.fromisoformat(flight_data['time'][0])
                        flight_data_obj.datetime_arrival       = datetime.fromisoformat(flight_data['time'][1])
                        flight_data_obj.number_seats_available = int(flight_data['faresLeft'])
                        flight_data_obj.ticket_price           = Decimal(flight_data['regularFare']['fares'][0]['amount'])

                        flight_data_obj.flight_key = flight_obj
                        flight_data_obj.save(force_insert=True)


                    except Exception as e: print(e)