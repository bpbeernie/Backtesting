from AMDReverseTestingStrategy import Constants as const
from AMDReverseTestingStrategy import TestStrategyBot

def create_bots(ib):
    bots = []
    
    for stock in const.STOCKS_TO_TEST:
        bots.append(TestStrategyBot.TestBot(ib, stock))
        
    return bots