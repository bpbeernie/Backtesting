from AMDOpenAggressiveTestingStrategy import Settings as const, TestStrategyBot, TestStrategyOfflineBot

def create_bots(ib):
    bots = []
    
    for stock in const.STOCKS_TO_TEST:
        bots.append(TestStrategyBot.TestBot(ib, stock))
        
    return bots

def create_bots_offline():
    bots = []
    
    for stock in const.STOCKS_TO_TEST:
        bots.append(TestStrategyOfflineBot.TestBot(stock))
        
    return bots