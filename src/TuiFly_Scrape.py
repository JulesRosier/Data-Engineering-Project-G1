from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import re
# from pprint import pprint

# CONSTS
DEPART = ['BRU', 'CRL']
HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
URL = "https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D={origin}&flyingTo%5B%5D={place}&depDate={date}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=false&returnDate={date}"

def parse_flights(json_data):
    flights = []
    for flight in json_data['flightViewData']:
        out = {}

        out['destination'] = flight['journeySummary']['arrivalAirportName']
        out['depart'] = flight['journeySummary']['departAirportName']
        out['date'] = datetime.fromisoformat(flight['departureDate']).strftime("%Y-%m-%d")
        out['price'] = flight['totalPrice']

        flights.append(out)
    return flights

def get_json(destionations, dates):
    origin = DEPART[0]
    place = destionations[0]
    date = dates[0]

    page = requests.get(URL.format(origin=origin, place=place, date=date), headers=HEADER)
    soup = BeautifulSoup(page.content, "lxml")
    script = soup.find(string=re.compile("var searchResultsJson"))
    for row in script.splitlines():
        if row.find("var searc") > 0:
            json_string = row[row.find('{'):][:-1]
            json_data = json.loads(json_string)
            return json_data
    raise Exception("JSON niet gevonden")

def get_data(destionations, dates) -> dict:
    json_data = get_json(destionations, dates)
    flights = parse_flights(json_data)

    return flights

