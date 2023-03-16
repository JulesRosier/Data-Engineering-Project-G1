from dates import get_dates
import TuiFly_Scrape
import Ryanair_Scrape
import Brussels_Airlines
from repository import connect_db, close_db, seed_db

from pprint import pprint

ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFS']
NUMBER_OF_DAYS = 10

dates = get_dates(NUMBER_OF_DAYS)

connect_db()
seed_db()

pprint(TuiFly_Scrape.get_data(ARIVE, dates))

# Ryanair_Scrape.get_data(ARIVE, dates)

# pprint(Brussels_Airlines.get_data(ARIVE, dates))

close_db()
