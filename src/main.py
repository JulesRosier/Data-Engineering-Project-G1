import logging
import datetime
import requests
import datetime
from dates import get_dates
import TuiFly_Scrape
import Ryanair_Scrape
import Brussels_Airlines
import time
import sys
from repository import connect_db, close_db, seed_db

ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFS']
END_DATE = '2023-10-01'

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to stdout
        logging.FileHandler('py_scraper.log')  # Output to a log file
    ]
)
logger = logging.getLogger(__name__)

# zorgt er voor dat de code alleen maar loopt als je expliciet main.py uitvoert
if __name__ == "__main__": 
    if len(sys.argv) != 2:
        logging.info("Usage: main.py <script>")
        sys.exit(1)
    script = sys.argv[1]
    
    logger.info(f"Running {script} script at {datetime.datetime.now()}")

    dates = get_dates(END_DATE)

    res = requests.get('https://kernel.org/')
    if (res.status_code):
        logging.info('Success, internet')
    else:
        logging.critical("Geen internet, exiting...")
        sys.exit(1)

    connect_db()
    seed_db()

    start_time = time.time()

    if script == "tuifly":
        logging.info("Scrapping tuifly")
        TuiFly_Scrape.get_data(ARIVE, dates)
        
    if script == "ryanair":
        Ryanair_Scrape.get_data(ARIVE, dates)

    if script == "brussels":
        Brussels_Airlines.get_data(ARIVE, dates)
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    logging.info(f"Elapsed time: {elapsed_time//60}:{elapsed_time%60}")
    close_db()