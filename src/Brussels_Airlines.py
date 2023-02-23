from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

URL = "https://book.brusselsairlines.com/lh/dyn/air-lh/revenue/viewFlights?B_DATE_1=202302240000&B_DATE_2=202303030000&B_LOCATION_1={depart}&CABIN=E&COUNTRY_SITE=BE&DEVICE_TYPE=DESKTOP&E_LOCATION_1={destination}&IP_COUNTRY=BE&LANGUAGE=GB&NB_ADT=1&NB_CHD=0&NB_INF=0&PORTAL=SN&POS=BE&SECURE=TRUE&SITE=LUFTBRUS&SO_SITE_COUNTRY_OF_RESIDENCE=BE&SO_SITE_LH_FRONTEND_URL=www.brusselsairlines.com&TRIP_TYPE=R"

# SETUP
options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')
driver_service = Service()
driver = webdriver.Chrome(service=driver_service,options=options)

flights = []
for plaats in ['AGP', 'PMI']:
    driver.implicitly_wait(100)
    driver.get(URL.format(depart='BRU', destination=plaats))
    _selection = driver.find_elements(By.CSS_SELECTOR, "div.row")
    data = driver.execute_script('return clientSideData')['tpi']
    
    # pprint(data)
    pprint(data['arrivalLocation'])
    for flight in data['availabilities']:
        out = {}
        out['destination'] = data['arrivalLocation']['airport']['name']
        out['depart'] = flight['segments'][0]['departureLocation']['airport']['name']
        out['date'] = flight['segments'][0]['formattedDepartureDate']
        out['price'] = flight['cabins'][0]['fares'][0]['price']
        out['operating_airline'] = flight['segments'][0]['operatingAirline']['name']

        flights.append(out)


pprint(flights)