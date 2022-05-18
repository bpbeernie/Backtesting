from AMDOpenAggressiveTestingStrategy import Settings as settings
import time


def run(ib):
    #Connect to IB on init
    ib.reqIds(-1)
    
    botList = []
    
    for strategy in settings.STRATEGY_LIST:
        botList.extend(strategy(ib)) 
    
    ib.addBots(botList)

    for bot in botList:
        bot.setup()
        
    state = [bot.isBotDone() for bot in botList]

    while not all(state):
        time.sleep(5)
        state = [bot.isBotDone() for bot in botList]