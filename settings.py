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

STOCKS_TO_TEST = []

OUTPUT_PATH = "C:/Users/bpbee/Desktop/trading/BackTesting/"
DATE_RANGE = []

STRATEGY_LIST = []

CASH_RISK = 0
MAX_AMOUNT = 0

def print_settings():
    print("Stocks:")
    print(STOCKS_TO_TEST)
    print("Date Range:")
    print(DATE_RANGE)
    print("Strategies")
    print(STRATEGY_LIST)