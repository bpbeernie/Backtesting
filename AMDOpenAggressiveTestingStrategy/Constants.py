from datetime import datetime, timedelta
import os
from dateutil.relativedelta import relativedelta
import pprint

STOCKS_TO_TEST = ["TWTR", "MSFT", "GM", "AAL", "AMD", "AAPL", "FB", "PFE", "UAL", "CSCO", 
                  "BAC", "DIS", "CRM", "BABA", "CMCSA", "PYPL", "ORCL", "MRK", "NVDA", "GILD", "C", 
                  "INTC", "MRVL", "MDLZ", "BA", "V", "JPM"]

HOLIDAYS = [datetime(2022, 1, 17), datetime(2022, 2, 21), datetime(2022, 4, 15),
            datetime(2022, 6, 20),datetime(2022, 7, 4), datetime(2022, 9, 5),
            datetime(2022,11, 24),datetime(2022,12, 26)]

OUTPUT_PATH = "C:/Users/bpbee/Desktop/trading/BackTesting/"
DATE_RANGE = []

folders = os.listdir(OUTPUT_PATH)
folders.remove("Archive")

currentDate = datetime.today()
DATE_RANGE.append((f'{currentDate:%Y%m}', datetime(currentDate.year, currentDate.month, 1), currentDate + timedelta(days=1)))

currentYear = currentDate.year

while True:
    currentDate = currentDate + relativedelta(months=-1)
    if currentDate.year != currentYear:
        break
    
    folder = f'{currentDate:%Y%m}'
    if folder not in folders:
        DATE_RANGE.append((folder, datetime(currentDate.year, currentDate.month, 1), datetime(currentDate.year, currentDate.month+1, 1)))
        
pp = pprint.PrettyPrinter(width=41, compact=True)
pp.pprint(DATE_RANGE)
