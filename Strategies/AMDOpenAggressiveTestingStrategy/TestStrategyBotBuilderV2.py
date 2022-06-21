import settings
from Strategies.AMDOpenAggressiveTestingStrategy import TestStrategyBotV2

def create_bots(ib):
    bots = []
    
    for stock in settings.STOCKS_TO_TEST:
        bots.append(TestStrategyBotV2.TestBot(ib, stock))
        
    return bots

def create_bots_offline():
    bots = []
    
    for stock in settings.STOCKS_TO_TEST:
        bots.append(TestStrategyBotV2.TestBot(None, stock))
        
    return bots