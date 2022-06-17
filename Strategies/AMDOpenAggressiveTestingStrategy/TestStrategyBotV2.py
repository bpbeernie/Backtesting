from ibapi.contract import Contract
from Helpers import Bars as bars
from Globals import Globals as gb
import logging
import os
import datetime
import threading
import csv
from Strategies import Settings as const
import pickle
from func_timeout import FunctionTimedOut, func_timeout
import math
from numpy.compat.py3k import long
import pprint

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
    lock = threading.Lock()
    dateLock = threading.Lock()
    cache_path = "Cache/"
    
    
    def __init__(self, ib, symbol):
        self.ib = ib
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
        
        if self.contract.symbol == "META":
            print("Update primary exchange for META")
            self.contract.primaryExchange = "NASDAQ"
        else:
            self.contract.primaryExchange = "ARCA"

        for dateRange in const.DATE_RANGE:
            TestBot.lock.acquire()
            try:
                func_timeout(420, self.testDateRange, args=(dateRange,))
            except FunctionTimedOut:
                print("Failed to process!")
                TestBot.dateLock.release()
                TestBot.lock.release()
            #self.testDateRange(dateRange)
            
            
    def testDateRange(self, dateRange):
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
            queryTime = single_date.strftime("%Y%m%d 23:59:59")
            reqId = gb.Globals.getInstance().getOrderId()
            self.reqIdList.append(reqId)
            
            path = f'{self.cache_path}{self.symbol}/{single_date:%Y-%m-%d}.pkl'
            
            if self.symbol == "META" and single_date < datetime.datetime(2022, 6, 9):
                path = f'{self.cache_path}FB/{single_date:%Y-%m-%d}.pkl'
            
            if os.path.exists(path):
                f = open(path, 'rb')
                self.data[f'{single_date:%Y-%m-%d}'] = pickle.load(f)
                f.close()
                reqIdProcessedFromCache.append(reqId)
            else:
                TestBot.dateLock.acquire()
                self.ib.reqHistoricalData(reqId, self.contract,queryTime,"1 D","5 secs","TRADES",1,1,False,[])

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
        
    def processBar(self, newBar):
        bar = bars.Bar()
        bar.close = newBar.close
        bar.high = newBar.high
        bar.low = newBar.low
        
        return bar   
    
    def calculateGainOrLoss(self, target, proposedBid, actualBid):
        result = (actualBid - target) / (proposedBid - target )
        
        return abs(result)
    
    def proccessDate(self, dateToProcess):
        print(f"==================={dateToProcess}===================")
        
        result = 0
        longEntryDone = False
        shortEntryDone = False
        longEntryRunning = False
        shortEntryRunning = False
        longEntryTriggered = False
        shortEntryTriggered = False
        actualLongEntry = 0
        actualShortEntry = 0
        
        startingBars = []
        data = self.data[dateToProcess]
        numStartingBars = 12
        
        path = f'{self.cache_path}{self.symbol}'
        os.makedirs(path, exist_ok=True)

        path = f'{path}/{dateToProcess}.pkl'
        
        if not os.path.exists(path):
            f = open(path, "wb")
            pickle.dump(data, f)
            f.close()
        
        for newBar in data:
            if len(startingBars) < numStartingBars:
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
                adjustedHigh = high + diff * 0.2
                adjustedLow = low - diff * 0.2
                adjustedDiff = adjustedHigh - adjustedLow
                
                entryLimitforLong = round(adjustedHigh, 2)
                
                if adjustedDiff == 0:
                    bar = bars.Bar()
                    bar.close = newBar.close
                    bar.high = newBar.high
                    bar.low = newBar.low
                    startingBars.append(bar)
                    numStartingBars = numStartingBars +12
                    continue
                
                quantity = math.ceil(25 / adjustedDiff)

                entryAmount = entryLimitforLong * quantity
            
                if entryAmount > 20000:
                    startingBars.append(self.processBar(newBar))
                    numStartingBars = numStartingBars +12
                    
                    print(f'{self.symbol} - date:{dateToProcess} q:{quantity} entry:{entryLimitforLong} diff:{adjustedDiff} amount:{entryAmount}')
                    continue
                
                profitTargetForLong = round(adjustedHigh + adjustedDiff * 3, 2)
                stopLossForLong = round(adjustedLow, 2)
                
                entryLimitforShort = round(adjustedLow, 2)
                profitTargetForShort = round(adjustedLow - adjustedDiff * 3, 2)
                stopLossForShort = round(adjustedHigh, 2)

                if longEntryDone and shortEntryDone:
                    return result
                
                if not longEntryTriggered and not shortEntryTriggered:
                    if newBar.high >= entryLimitforLong:
                        longEntryTriggered = True
                        continue
                
                    if newBar.low <= entryLimitforShort:
                        shortEntryTriggered = True
                        continue
                
                if longEntryTriggered and not longEntryRunning:
                    longEntryRunning = True
                    actualLongEntry = (newBar.high + newBar.low) / 2
                    continue
                    
                if shortEntryTriggered and not shortEntryRunning:
                    shortEntryRunning = True
                    actualShortEntry = (newBar.high + newBar.low) / 2
                    continue
                
                
                if longEntryTriggered and not longEntryDone:
                    if newBar.high >= profitTargetForLong:
                        if longEntryRunning:
                            result += 3 * self.calculateGainOrLoss(profitTargetForLong, entryLimitforLong, actualLongEntry)
                        return result
                    if newBar.low <= stopLossForLong:
                        shortEntryTriggered = True
                        longEntryDone = True
                        result -= 1 * self.calculateGainOrLoss(stopLossForLong, entryLimitforLong, actualLongEntry)
                        continue
                        
                if shortEntryTriggered and not shortEntryDone:
                    if newBar.low <= profitTargetForShort:
                        if shortEntryRunning:
                            result += 3* self.calculateGainOrLoss(profitTargetForShort, entryLimitforShort, actualShortEntry)
                        return result
                    
                    if newBar.high >= stopLossForShort:
                        longEntryTriggered = True
                        shortEntryDone = True
                        result -= 1* self.calculateGainOrLoss(stopLossForShort, entryLimitforShort, actualShortEntry)
                        continue
                

                
                """
                if longEntryTriggered and not longEntryRunning:
                    if entryLimitforLong >= newBar.low:
                        longEntryRunning = True
                        continue
                    
                if shortEntryTriggered and not shortEntryRunning:
                    if entryLimitforShort <= newBar.high:
                        shortEntryRunning = True
                        continue
                """

                
        if shortEntryRunning and not shortEntryDone:
            remaining =  (actualShortEntry - data[-1].close) / (actualShortEntry - profitTargetForShort)
            result += remaining * 3
            
        if longEntryRunning and not longEntryDone:
            remaining = (data[-1].close - actualLongEntry) /  (profitTargetForLong - actualLongEntry)
            result += remaining * 3
            
        return result
        
        
    def historicalDataEnd(self,reqId):
        if reqId not in self.reqIdList:
            return
        
        self.processedReqIdList.append(reqId)
        TestBot.dateLock.release()
        self.finalize()
        
    def finalize(self):
        if len(self.reqIdList) == len(self.processedReqIdList):
            for date in self.data.keys():
                result = self.proccessDate(date)
                self.finalResults.setdefault(datetime.datetime.strptime(date, '%Y-%m-%d'), result) 

            self.printFinalResults()
            print("Ending " + self.symbol)
            TestBot.lock.release()
        
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
