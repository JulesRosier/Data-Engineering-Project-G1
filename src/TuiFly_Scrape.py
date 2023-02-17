import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime

import re

DEPART = ['BRU', 'CRL']
ARIVE = ['AGP', 'BER', 'LIS']
DATES = ['2023-03-02', '2023-03-03', '2023-03-04']
ROUND_TRIP = 'false'
INCLUDE_CONNECTING_FLIGHTS = 'false'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

origin = DEPART[0]
place = ARIVE[0]
date = DATES[0]

url = f"https://www.tuifly.be/flight/nl/search?flyingFrom%5B%5D={origin}&flyingTo%5B%5D={place}&depDate={date}&adults=1&children=0&childAge=&choiceSearch=true&searchType=pricegrid&nearByAirports=true&currency=EUR&isOneWay=false&returnDate={date}"

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, "lxml")
script = soup.find(string=re.compile("var searchResultsJson"))

flights = []

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


for row in script.splitlines():
    if row.find("var searc") > 0:
        # extract JSON from JS var
        json_string = row[row.find('{'):][:-1]
        json_data = json.loads(json_string)
        flights = parse_flights(json_data)
        f = open("res", "w")
        f.write(json_string)
        f.close()

pprint(flights)



