from bs4 import BeautifulSoup
from datetime import datetime, date, time
import requests
import json
import re
import random
from requests.exceptions import Timeout
from proxies import get_valid_proxy

from repository import Flight
# from pprint import pprint

# CONSTS
DEPARTS = ['BRU', 'ANR', 'OST', 'LGG']
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
URL = "https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D={origin}&flyingTo%5B%5D={place}&depDate={date}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=false&currency=EUR&isOneWay=true"

def parse_flight(json_data):
    flights = []
    for flight in json_data['flightViewData']:
        out = {}

        try:
            depdate = date.fromisoformat(flight['journeySummary']['departDate'])
            deptime = time.fromisoformat(flight['journeySummary']['depTime'] + ':00') 
            arrivaldate = date.fromisoformat(flight['journeySummary']['arrivalDate'])
            arrivaltime = time.fromisoformat(flight['journeySummary']['arrivalTime'] + ':00')

            f_flightNumber = flight['flightsectors'][0]['flightNumber']
            f_depart = flight['journeySummary']['departAirportCode']
            f_destination = flight['journeySummary']['arrivalAirportCode']
            f_departure_datetime = datetime.combine(depdate, deptime).strftime("%Y-%m-%d %H:%M:%S")
            f_arrival_datetime = datetime.combine(arrivaldate, arrivaltime).strftime("%Y-%m-%d %H:%M:%S") 

            f_key = f_flightNumber + f_depart + f_departure_datetime + f_destination + f_arrival_datetime

            f_duration_s = flight['journeySummary']['totalJnrDuration']
            f_duration_h, f_duration_min = f_duration_s.split(' ')

            if Flight.select().where(Flight.flight_key == f_key).exists():
                flight_obj = Flight.get(flight_key = f_key)
                bestaat_all = True
            else:
                flight_obj = Flight(flight_key = f_key)
                bestaat_all = False

            flight_obj.last_updated           = datetime.now()
            flight_obj.airline_id             = 3
            flight_obj.airport_code_depart    = flight['journeySummary']['departAirportCode']
            flight_obj.airport_code_arrival   = flight['journeySummary']['arrivalAirportCode']
            flight_obj.datetime_depart        = datetime.combine(depdate, deptime)
            flight_obj.datetime_arrival       = datetime.combine(arrivaldate, arrivaltime)
            flight_obj.flight_duration        = time(hour=int(f_duration_h[:-1]), minute=int(f_duration_min[:-1]))
            flight_obj.ticket_price           = flight['totalPrice']
            flight_obj.number_seats_total     = None
            flight_obj.number_seats_available = flight['journeySummary']['availableSeats']
            flight_obj.number_of_stops        = None
            flight_obj.connection_flight      = None
            flight_obj.flight_number          = flight['flightsectors'][0]['flightNumber']

            if bestaat_all:
                flight_obj.save()
            else:
                flight_obj.save(force_insert=True)

        except Exception as e: print(e)

    return flights

timeout = 30

def get_data(destinations, dates):
    flights = []
    for depart in DEPARTS:
        for date in dates:
            for destination in destinations:
                print(f'Pulling {depart} to {destination} on {date}')
                proxy = get_valid_proxy()
                print(proxy)
                page = requests.get(URL.format(origin=depart, place=destination, date=date), headers=HEADER, proxies=proxy, timeout=timeout)
                soup = BeautifulSoup(page.content, "lxml")
                script = soup.find(string=re.compile("var searchResultsJson"))
                for row in script.splitlines():
                    if row.find("var searc") > 0:
                        json_string = row[row.find('{'):][:-1]
                        json_data = json.loads(json_string)
                        flights += parse_flight(json_data)
    return flights
