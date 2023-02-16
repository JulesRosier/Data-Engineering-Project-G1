import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime

DEPART = ['BRU', 'CRL']
ARIVE = ['AGP', 'BER', 'LIS']
DATES = ['2023-03-02', '2023-03-03', '2023-03-04']

flights = []
for place in ARIVE:
    for origin in DEPART:
        for date in DATES:
            URL = f"https://www.ryanair.com/api/booking/v4/nl-nl/availability?ADT=1&CHD=0&DateIn={date}&DateOut={date}&Destination={place}&Disc=0&INF=0&Origin={origin}&TEEN=0&promoCode=&IncludeConnectingFlights=false&RoundTrip=false&ToUs=AGREED"
            print(f"Pulling {origin} to {place} on {date}")
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "lxml")
            result = soup.find("p").text

            json_reponse = json.loads(result)

            for flight in json_reponse['trips']:
                # pprint(flight)
                if not flight['dates'][0]['flights']:
                    break
                out = {}
                out['destination'] = flight['destinationName']
                out['depart'] = flight['originName']
                out['date'] = datetime.fromisoformat(flight['dates'][0]['dateOut']).strftime("%Y-%m-%d")
                out['price'] = flight['dates'][0]['flights'][0]['regularFare']['fares'][0]['amount']
                flights.append(out)

print('results:')
pprint(flights) 


