from dates import get_dates
import TuiFly_Scrape
import Ryanair_Scrape
import Brussels_Airlines

from pprint import pprint

ARIVE = ['AGP', 'CFU', 'HER', 'RHO', 'BDS', 'NAP', 'PMO', 'FAO', 'ALC', 'IBZ', 'PMI', 'TFN']
NUMBER_OF_DAYS = 1

dates = get_dates(NUMBER_OF_DAYS)

pprint(TuiFly_Scrape.get_data(ARIVE, dates))

# pprint(Ryanair_Scrape.get_data(ARIVE, dates))

# pprint(Brussels_Airlines.get_data(ARIVE, dates))