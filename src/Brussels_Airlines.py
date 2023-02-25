from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import datetime

from pprint import pprint

URL = "https://book.brusselsairlines.com/lh/dyn/air-lh/revenue/viewFlights?B_DATE_1={date1}&B_DATE_2={date2}&B_LOCATION_1={depart}&CABIN=E&COUNTRY_SITE=BE&DEVICE_TYPE=DESKTOP&E_LOCATION_1={destination}&IP_COUNTRY=BE&LANGUAGE=GB&NB_ADT=1&NB_CHD=0&NB_INF=0&PORTAL=SN&POS=BE&SECURE=TRUE&SITE=LUFTBRUS&SO_SITE_COUNTRY_OF_RESIDENCE=BE&SO_SITE_LH_FRONTEND_URL=www.brusselsairlines.com&TRIP_TYPE=R"

def get_driver():
    # options.add_experimental_option("detach", True)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service()
    driver = webdriver.Chrome(service=driver_service,options=options)
    return driver


def get_data(destionations: list[str], dates: list[datetime.date]) -> dict:
    driver = get_driver()
    flights = []
    for date in dates:
        # date = date.strftime('%Y%m%d0000')
        for plaats in destionations:
            driver.implicitly_wait(100)
            driver.get(URL.format(depart='BRU',
                                  destination=plaats,
                                  date1=date.strftime('%Y%m%d0000'),
                                  date2=(datetime.timedelta(days=7) + date).strftime('%Y%m%d0000')))

            # deze select is zodat hij wacht tot alles is ingeladen
            _selection = driver.find_elements(By.CSS_SELECTOR, "span.icon-logo-sn")

            data = driver.execute_script('return clientSideData')['tpi']
            
            # pprint(data)
            try:
                pprint(data['arrivalLocation'])
                for flight in data['availabilities']:
                    out = {}
                    out['destination'] = data['arrivalLocation']['airport']['name']
                    out['depart'] = flight['segments'][0]['departureLocation']['airport']['name']
                    out['date'] = flight['segments'][0]['formattedDepartureDate']
                    out['price'] = flight['cabins'][0]['fares'][0]['price']
                    out['operating_airline'] = flight['segments'][0]['operatingAirline']['name']

                    flights.append(out)
            except:
                try:
                    error_div = driver.find_element(By.CSS_SELECTOR, "div.message-error")
                    print('ERROR', error_div.text)
                except:
                    print('iets anders dan een site error ging miss')

    return flights