import datetime
import requests
from dates import get_dates
import TuiFly_Scrape
import Ryanair_Scrape
import Brussels_Airlines
from repository import connect_db, close_db, seed_db
import time

from pprint import pprint

ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFS']
NUMBER_OF_DAYS = 10

# zorgt er voor dat de code alleen maar loopt als je expliciet main.py uitvoert
if __name__ == "__main__": 
    print(f"Running script at {datetime.datetime.now()}")
    dates = get_dates(NUMBER_OF_DAYS)
    # time.sleep(5)

    res = requests.get('https://kernel.org/')
    if (res.status_code):
        print('Success, internet')
    else:
        raise Exception("Geen internet")

    connect_db()
    seed_db()

    pprint(TuiFly_Scrape.get_data(ARIVE, dates))

    # Ryanair_Scrape.get_data(ARIVE, dates)

    # pprint(Brussels_Airlines.get_data(ARIVE, dates))

    close_db()
