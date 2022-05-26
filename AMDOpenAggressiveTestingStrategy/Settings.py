from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def monthToDate():
    currentDate = datetime.today()
    
    return [(f'{currentDate:%Y%m}', datetime(currentDate.year, currentDate.month, 1), currentDate + timedelta(days=1))]

def monthsInYear(year):
    date_list = []
    today = datetime.today()
    
    if year == today.year:
        date_list.extend(monthToDate())
        currentDate = today + relativedelta(months=-1)
    else:
        currentDate = datetime(year, 12, 1)
    
    while True:
        if currentDate.year != year:
            break
        
        folder = f'{currentDate:%Y%m}'
        
        nextMonth = currentDate.month+1
        nearYear = currentDate.year
        if nextMonth == 13:
            nextMonth = 1
            nearYear = nearYear + 1
            
        date_list.append((folder, datetime(currentDate.year, currentDate.month, 1), datetime(nearYear, nextMonth, 1)))
            
        currentDate = currentDate + relativedelta(months=-1)
    return date_list 


"""
ORCL is misleading. Too little volume to utilize.
"""

STOCKS_TO_TEST = ["TWTR", "MSFT", "GM", "AAL", "AMD", "AAPL", "FB", "PFE", "UAL", "CSCO", 
                  "BAC", "DIS", "CRM", "BABA", "CMCSA", "PYPL", "ORCL", "MRK", "NVDA", "GILD", "C", 
                  "INTC", "MRVL", "MDLZ", "BA", "V", "JPM"]

HOLIDAYS_2021 = [datetime(2021, 1, 1), datetime(2021, 1, 18), datetime(2021, 2, 15),
            datetime(2021, 4, 2),datetime(2021, 5, 31), datetime(2021, 7, 5),
            datetime(2021,9, 6),datetime(2021,11, 25), datetime(2021,12, 24)]

HOLIDAYS = [datetime(2022, 1, 17), datetime(2022, 2, 21), datetime(2022, 4, 15),
            datetime(2022, 6, 20),datetime(2022, 7, 4), datetime(2022, 9, 5),
            datetime(2022,11, 24),datetime(2022,12, 26)]

HOLIDAYS.extend(HOLIDAYS_2021)

OUTPUT_PATH = "C:/Users/bpbee/Desktop/trading/BackTesting/"
DATE_RANGE = monthToDate()

STRATEGY_LIST = []

def print_settings():
    print("Stocks:")
    print(STOCKS_TO_TEST)
    print("Date Range:")
    print(DATE_RANGE)
    print("Strategies")
    print(STRATEGY_LIST)