from Strategies.AMDOpenAggressiveTestingStrategy.TestStrategyBotBuilder import create_bots as AMDOpenAggressiveTestingStrategyCreateBot, create_bots_offline as AMDOpenAggressiveOfflineTestingStrategyCreateBot
from Strategies.AMDOpenAggressiveExperimentalTestingStrategy.TestStrategyExperimentalBotBuilder import create_bots_offline as AMDExperiment

BOTS_MAPPING = {"AMDAggressiveTestStrategy": AMDOpenAggressiveTestingStrategyCreateBot,
                "ExperimentalBotStrategy": AMDExperiment}

BOTS_OFFLINE_MAPPING = {"AMDAggressiveTestStrategy": AMDOpenAggressiveOfflineTestingStrategyCreateBot,
                        "ExperimentalBotStrategy": AMDExperiment}

STOCKS = ["TWTR", "MSFT", "GM", "AAL", "AMD", "AAPL", "FB", "PFE", "UAL", "CSCO", 
                  "BAC", "DIS", "CRM", "BABA", "CMCSA", "PYPL", "ORCL", "NVDA", "GILD", "C", 
                  "INTC", "MRVL", "MDLZ", "BA", "V", "JPM"]