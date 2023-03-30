from pprint import pprint
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import time
from selenium_stealth import stealth

from repository import Flight, FlightData

DEPART = 'BRU'

URL = "https://book.brusselsairlines.com/lh/dyn/air-lh/revenue/viewFlights?B_DATE_1={date1}&B_DATE_2={date2}&B_LOCATION_1={depart}&CABIN=E&COUNTRY_SITE=BE&DEVICE_TYPE=DESKTOP&E_LOCATION_1={destination}&IP_COUNTRY=BE&LANGUAGE=GB&NB_ADT=1&NB_CHD=0&NB_INF=0&PORTAL=SN&POS=BE&SECURE=TRUE&SITE=LUFTBRUS&SO_SITE_COUNTRY_OF_RESIDENCE=BE&SO_SITE_LH_FRONTEND_URL=www.brusselsairlines.com&TRIP_TYPE=R"

def set_chrome_options() -> None:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    chrome_options.add_argument("--log-level=3")
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
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver_service = Service()
    driver = webdriver.Chrome(service=driver_service, options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def get_data(destinations: list[str], dates: list[datetime.date]) -> dict:
    driver = get_driver()
    flights = []
    for date in dates:
        # date = date.strftime('%Y%m%d0000')
        for plaats in destinations:
            driver.implicitly_wait(100)
            driver.get(URL.format(depart=DEPART,
                                  destination=plaats,
                                  date1=date.strftime('%Y%m%d0000'),
                                  date2=(datetime.timedelta(days=7) + date).strftime('%Y%m%d0000')))
            time.sleep(5)

            # deze select is zodat hij wacht tot alles is ingeladen
            _selection = driver.find_elements(
                By.CSS_SELECTOR, "span.icon-logo-sn")

            data = driver.execute_script('return clientSideData')['tpi']

            # pprint(data)

            # try:
            for flight in data['availabilities']:
                operating_airline = flight['segments'][0]['operatingAirline']['name']
                if operating_airline == 'Brussels Airlines':
                    duration_min = flight['segments'][0]['duration']
                    departure_time_string = flight['segments'][0]['formattedDepartureDate']
                    arrival_time_string =  flight['segments'][0]['formattedArrivalDate']

                    f_flightNumber = flight['segments'][0]['flightNumber']
                    f_depart = data['departureLocation']['airport']['code']
                    f_destination = data['arrivalLocation']['airport']['code']
                    f_departure_datetime = datetime.datetime.strptime(departure_time_string.split(' ')[1] + ' ' + departure_time_string.split(' ')[2], '%d.%m.%Y %H:%M').strftime("%Y-%m-%d %H:%M:%S")
                    f_arrival_datetime = datetime.datetime.strptime(arrival_time_string.split(' ')[1] + ' ' + arrival_time_string.split(' ')[2], '%d.%m.%Y %H:%M').strftime("%Y-%m-%d %H:%M:%S")
                    f_key = f_flightNumber + f_depart + f_departure_datetime + f_destination + f_arrival_datetime
                    out = {}

                    segments = flight['segments']

                    if Flight.select().where(Flight.flight_key == f_key).exists():
                        flight_obj = Flight.get(flight_key = f_key)
                        bestaat_all = True
                    else: # Bestaat nog niet

                        flight_obj = Flight(flight_key = f_key)

                        flight_obj.airline_id             = 2
                        flight_obj.airport_code_depart    = data['departureLocation']['airport']['code']
                        flight_obj.airport_code_arrival   = data['arrivalLocation']['airport']['code']
                        flight_obj.flight_duration        = datetime.time(hour=duration_min//60, minute=duration_min%60)
                        flight_obj.number_seats_total     = None
                        flight_obj.number_of_stops        = len(segments) - 1
                        flight_obj.connection_flight      = len(segments) > 1
                        flight_obj.flight_number          = flight['segments'][0]['flightNumber']

                        flight_obj.save(force_insert=True)

                        flight_data_obj = FlightData()

                        flight_data_obj.datetime_depart        = datetime.datetime.strptime(departure_time_string.split(' ')[1] + ' ' + departure_time_string.split(' ')[2], '%d.%m.%Y %H:%M')
                        flight_data_obj.datetime_arrival       = datetime.datetime.strptime(arrival_time_string.split(' ')[1] + ' ' + arrival_time_string.split(' ')[2], '%d.%m.%Y %H:%M')
                        flight_data_obj.number_seats_available = flight['cabins'][0]['fares'][0]['numberOfSeatsLeft']
                        flight_data_obj.ticker_price           = flight['cabins'][0]['fares'][0]['price'] # Meerdere soorten Economy ! (4)

                        flight_data_obj.flight_key = flight_obj

                        flight_data_obj.save(force_insert=True)

                        # bestaat_all = False
                    flights.append(out)

                    pprint(out) # --> inhoud van vlucht bekijken
            # except:
            #     try:
            #         error_div = driver.find_element(
            #             By.CSS_SELECTOR, "div.message-error")
            #         print('ERROR', error_div.text)
            #     except:
            #         print('iets anders dan een site error ging miss')
    return flights
