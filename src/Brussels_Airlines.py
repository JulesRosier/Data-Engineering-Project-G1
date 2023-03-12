from pprint import pprint
from datetime import timedelta
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
DEPART = 'BRU'

URL = "https://book.brusselsairlines.com/lh/dyn/air-lh/revenue/viewFlights?B_DATE_1={date1}&B_DATE_2={date2}&B_LOCATION_1={depart}&CABIN=E&COUNTRY_SITE=BE&DEVICE_TYPE=DESKTOP&E_LOCATION_1={destination}&IP_COUNTRY=BE&LANGUAGE=GB&NB_ADT=1&NB_CHD=0&NB_INF=0&PORTAL=SN&POS=BE&SECURE=TRUE&SITE=LUFTBRUS&SO_SITE_COUNTRY_OF_RESIDENCE=BE&SO_SITE_LH_FRONTEND_URL=www.brusselsairlines.com&TRIP_TYPE=R"

def set_chrome_options() -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

def get_driver():
    # options.add_experimental_option("detach", True)
    options = set_chrome_options()
    driver_service = Service()
    driver = webdriver.Chrome(service=driver_service, options=options)
    return driver


def get_data(destionations: list[str], dates: list[datetime.date]) -> dict:
    driver = get_driver()
    flights = []
    for date in dates:
        # date = date.strftime('%Y%m%d0000')
        for plaats in destionations:
            driver.implicitly_wait(100)
            driver.get(URL.format(depart=DEPART,
                                  destination=plaats,
                                  date1=date.strftime('%Y%m%d0000'),
                                  date2=(datetime.timedelta(days=7) + date).strftime('%Y%m%d0000')))

            # deze select is zodat hij wacht tot alles is ingeladen
            _selection = driver.find_elements(
                By.CSS_SELECTOR, "span.icon-logo-sn")

            data = driver.execute_script('return clientSideData')['tpi']

            # pprint(data)
            try:
                # pprint(data['arrivalLocation'])
                for flight in data['availabilities']:
                    operating_airline = flight['segments'][0]['operatingAirline']['name']
                    if operating_airline == 'Brussels Airlines':
                        out = {}
                        
                        duration_min = flight['segments'][0]['duration']
                        
                        departure_time_string = flight['segments'][0]['formattedDepartureDate']
                        arrival_time_string =  flight['segments'][0]['formattedArrivalDate']
                        
                        segments = flight['segments']

                        out['departCode'] = data['departureLocation']['airport']['code']
                        out['departLocation'] = data['departureLocation']['city']['name']
                        out['destinationCode'] = data['arrivalLocation']['airport']['code']
                        out['destinationLocation'] = data['arrivalLocation']['city']['name']
                        out['departureTime'] = datetime.strptime(departure_time_string, '%A, %d.%m.%Y %I:%M %p') 
                        out['arrivalTime'] = datetime.strptime(arrival_time_string, '%A, %d.%m.%Y %I:%M %p') 
                        out['duration'] = datetime.timedelta(minutes = duration_min)
                        # out['flightKey'] = zelf genereren, flightNumber + departureTime?
                        out['flightNumber'] = flight['segments'][0]['flightNumber']
                        out['price'] = flight['cabins'][0]['fares'][0]['price'] # Meerdere soorten Economy ! (4)
                        # out ['numberSeatsTotal] = None
                        out['numberSeatsAvailable'] = flight['cabins'][0]['fares'][0]['numberOfSeatsLeft']
                        out['numberOfStops'] = len(segments) - 1        
                        out['connectionFlight'] = len(segments) > 1
                        out['operating_airline'] = flight['segments'][0]['operatingAirline']['name']
                        
                        flights.append(out)
            except:
                try:
                    error_div = driver.find_element(
                        By.CSS_SELECTOR, "div.message-error")
                    print('ERROR', error_div.text)
                except:
                    print('iets anders dan een site error ging miss')

    return flights
