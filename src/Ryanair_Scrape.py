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
                        flights.append(out)

                    except:
                        print('iets ging miss')

    return (flights)
