from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json

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
                page = requests.get(URL.format(date=date, place=place, origin=origin))
                soup = BeautifulSoup(page.content, "lxml")
                result = soup.find("p").text
                json_reponse = json.loads(result)

                for flight in json_reponse['trips']:
                    if flight['dates'][0]['flights'] == []:
                        break
                    out = {}
                    try:
                        out['destination'] = flight['destinationName']
                        out['depart'] = flight['originName']
                        out['date'] = datetime.fromisoformat(flight['dates'][0]['dateOut']).strftime("%Y-%m-%d")
                        out['price'] = flight['dates'][0]['flights'][0]['regularFare']['fares'][0]['amount']
                        flights.append(out)
                    except:
                        print('iets ging miss')
    
    return(flights)



