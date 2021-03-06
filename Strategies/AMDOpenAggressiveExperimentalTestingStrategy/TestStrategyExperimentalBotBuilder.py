import settings
from Strategies.AMDOpenAggressiveExperimentalTestingStrategy import TestStrategyOfflineExperimentalBot

def create_bots(ib):
    bots = []
    
    for stock in settings.STOCKS_TO_TEST:
        bots.append(TestStrategyOfflineExperimentalBot.TestBot(ib, stock))
        
    return bots

def create_bots_offline():
    bots = []
    
    for stock in settings.STOCKS_TO_TEST:
        bots.append(TestStrategyOfflineExperimentalBot.TestBot(stock))
        
    return bots