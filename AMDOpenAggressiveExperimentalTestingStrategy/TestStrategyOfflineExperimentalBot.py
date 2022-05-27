from ibapi.contract import Contract
from Helpers import Bars as bars
from Globals import Globals as gb
import logging
import os
import datetime
import csv
from AMDOpenAggressiveExperimentalTestingStrategy import Settings as const
import pickle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_filename = "logs/test.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler(log_filename, mode="a", encoding=None, delay=False)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#Bot Logic
class TestBot:
    cache_path = "Cache/"

    def __init__(self, symbol):
        self.symbol = symbol
        self.reqIdList = []
        self.processedReqIdList = []
        
        self.barsize = 1
        self.openBar = None
        self.entryLimitforShort = 0.0
        self.profitTargetForShort = 0.0
        self.stopLossForShort = 0.0
        self.entryLimitforLong = 0.0
        self.profitTargetForLong = 0.0
        self.stopLossForLong = 0.0
        self.data = {}
        
        self.dateCount = 0
        
        self.longEntryRunning = False
        self.longEntryDone = False
        self.shortEntryRunning = False
        self.shortEntryDone = False
        
        self.finalResults = {}
        
        self.proccessedDateRange = []

    def setup(self):
        self.contract = Contract()
        self.contract.symbol = self.symbol.upper()
        self.contract.secType = "STK"
        self.contract.exchange = "SMART"
        self.contract.currency = "USD"
        self.contract.primaryExchange = "ARCA"

        for dateRange in const.DATE_RANGE:
            self.reqIdList = []
            self.processedReqIdList = []
            self.data = {}
            self.finalResults = {}
            
            self.folderName = dateRange[0]
            
            start_date = dateRange[1]
            end_date = dateRange[2] - datetime.timedelta(days=1)
        
            date_range = self.workdays(start_date, end_date)
            self.dateCount = len(date_range)
            reqIdProcessedFromCache = []
            
            print("Starting " + self.symbol)
            for single_date in date_range:
                print(single_date)
                reqId = gb.Globals.getInstance().getOrderId()
                self.reqIdList.append(reqId)
                
                path = f'{self.cache_path}{self.symbol}/{single_date:%Y-%m-%d}.pkl'
                
                if os.path.exists(path):
                    f = open(path, 'rb')
                    self.data[f'{single_date:%Y-%m-%d}'] = pickle.load(f)
                    f.close()
                    reqIdProcessedFromCache.append(reqId)
                else:
                    raise ValueError("Can't process date in offline mode")

            self.proccessedDateRange.append(dateRange)
            
            if len(reqIdProcessedFromCache) > 0:
                self.processedReqIdList.extend(reqIdProcessedFromCache)
                self.finalize()
        
    def isBotDone(self):
        return len(self.reqIdList) == len(self.processedReqIdList) and len(self.proccessedDateRange) == len(const.DATE_RANGE)


    def workdays(self, d, end, excluded=(6, 7)):
        days = []
        while d.date() <= end.date():
            if d.isoweekday() not in excluded and d not in const.HOLIDAYS:
                days.append(d)
            d += datetime.timedelta(days=1)
        return days

    def on_bar_update(self, reqId, bar, realtime):
        if reqId not in self.reqIdList:
            return
        
        date = datetime.datetime.strptime(bar.date, '%Y%m%d  %H:%M:%S')
        dateString = f'{date:%Y-%m-%d}'
        
        newBar = bars.Bar()
        newBar.open = bar.open
        newBar.close = bar.close
        newBar.high = bar.high
        newBar.low = bar.low
        
        self.data.setdefault(dateString, []).append(newBar) 
        
    def proccessDate(self, dateToProcess):
        result = 0
        longEntryDone = False
        shortEntryDone = False
        longEntryRunning = False
        shortEntryRunning = False
        startingBars = []
        data = self.data[dateToProcess]
        
        for newBar in data:     
            if len(startingBars) < 12:
                bar = bars.Bar()
                bar.close = newBar.close
                bar.high = newBar.high
                bar.low = newBar.low
                startingBars.append(bar)
                continue
            else:
                high = max(o.high for o in startingBars)
                low = min(o.low for o in startingBars)

                diff = high - low
                adjustedHigh = high + diff * 0.21
                adjustedLow = low - diff * 0.21
                adjustedDiff = adjustedHigh - adjustedLow
                
                entryLimitforLong = round(adjustedHigh, 2)
                profitTargetForLong = round(adjustedHigh + adjustedDiff * 3, 2)
                stopLossForLong = round(adjustedLow, 2)
                
                entryLimitforShort = round(adjustedLow, 2)
                profitTargetForShort = round(adjustedLow - adjustedDiff * 3, 2)
                stopLossForShort = round(adjustedHigh, 2)

                if longEntryDone and shortEntryDone:
                    return result
                
                if longEntryRunning and not longEntryDone:
                    if newBar.high >= profitTargetForLong:
                        result += 3
                        return result
                    if newBar.low <= stopLossForLong:
                        shortEntryRunning = True
                        longEntryDone = True
                        result -= 1
                        
                if shortEntryRunning and not shortEntryDone:
                    if newBar.low <= profitTargetForShort:
                        result += 3
                        return result
                    
                    if newBar.high >= stopLossForShort:
                        longEntryRunning = True
                        shortEntryDone = True
                        result -= 1
                
                if not longEntryRunning and not shortEntryRunning:
                    if newBar.high >= entryLimitforLong:
                        longEntryRunning = True
                    
                    if newBar.low <= entryLimitforShort:
                        shortEntryRunning = True
                        
        if shortEntryRunning and not shortEntryDone:
            remaining =  (entryLimitforShort - data[-1].close) / (entryLimitforShort - profitTargetForShort)
            result += remaining * 3
            
        if longEntryRunning and not longEntryDone:
            remaining = (data[-1].close - entryLimitforLong) /  (profitTargetForLong - entryLimitforLong)
            result += remaining * 3
            
        return result
        
        
    def historicalDataEnd(self,reqId):
        if reqId not in self.reqIdList:
            return
        
        self.processedReqIdList.append(reqId)
        self.finalize()
        
    def finalize(self):
        if len(self.reqIdList) == len(self.processedReqIdList):
            for date in self.data.keys():
                result = self.proccessDate(date)
                self.finalResults.setdefault(datetime.datetime.strptime(date, '%Y-%m-%d'), result) 

            self.printFinalResults()
            print("Ending " + self.symbol)
        
    def printFinalResults(self):
        folder = const.OUTPUT_PATH + f'{self.folderName}/'
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        with open(folder + self.symbol + ".csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([None, "Win", "Lose"])
        
            keys = sorted(self.finalResults.keys())
            for key in keys:
                value = self.finalResults[key]
                date = key.strftime("%Y-%m-%d")
                if value < 0:
                    writer.writerow([date, None, abs(value)])
                else:
                    writer.writerow([date, abs(value), None])
        

    def updateStatus(self, orderID, status):
        pass

    def on_realtime_update(self, reqId, time, open_, high, low, close, volume, wap, count):
        pass
