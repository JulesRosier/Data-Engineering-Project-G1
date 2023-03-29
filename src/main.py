import datetime
import requests
from dates import get_dates
import TuiFly_Scrape
import Ryanair_Scrape
import Brussels_Airlines
from repository import connect_db, close_db, seed_db
import time
import sys

from pprint import pprint

ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFS']
NUMBER_OF_DAYS = 10

# zorgt er voor dat de code alleen maar loopt als je expliciet main.py uitvoert
if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print("Usage: main.py <script>")
        sys.exit(1)
    script = sys.argv[1]
    
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

    if script == "TuiFly_Scrape":
        # pprint(TuiFly_Scrape.get_data(ARIVE, dates))
        TuiFly_Scrape.get_data(ARIVE, dates)
        
    if script == "Ryanair_Scrape":
        Ryanair_Scrape.get_data(ARIVE, dates)

    # if script == "Brussels_Airlines":
        # Brussels_Airlines.get_data(ARIVE, dates)

    close_db()
