import datetime
import requests
import datetime
from dates import get_dates
import TuiFly_Scrape
import Ryanair_Scrape
import Brussels_Airlines
from repository import connect_db, close_db, seed_db
import time
import sys

from pprint import pprint

ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFS']
# NUMBER_OF_DAYS = 185 # tot en met 1 oktober
END_DATE = '2023-10-01'

# zorgt er voor dat de code alleen maar loopt als je expliciet main.py uitvoert
if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print("Usage: main.py <script>")
        sys.exit(1)
    script = sys.argv[1]
    
    print(f"Running script at {datetime.datetime.now()}")
    dates = get_dates(END_DATE)

    res = requests.get('https://kernel.org/')
    if (res.status_code):
        print('Success, internet')
    else:
        raise Exception("Geen internet")

    connect_db()
    seed_db()

    start_time = time.time()

    if script == "tuifly":
        TuiFly_Scrape.get_data(ARIVE, dates)
        
    if script == "ryanair":
        Ryanair_Scrape.get_data(ARIVE, dates)

    if script == "brussels":
        Brussels_Airlines.get_data(ARIVE, dates)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds")
    close_db()
