from Strategies.AMDOpenAggressiveTestingStrategy.TestStrategyBotBuilder import create_bots as AMDOpenAggressiveTestingStrategyCreateBot, create_bots_offline as AMDOpenAggressiveOfflineTestingStrategyCreateBot
from Strategies.AMDOpenAggressiveExperimentalTestingStrategy.TestStrategyExperimentalBotBuilder import create_bots_offline as AMDExperiment
from Strategies.AMDOpenAggressiveTestingStrategy.TestStrategyBotBuilderV2 import create_bots as AMDOpenAggressiveTestingStrategyCreateBotV2

BOTS_MAPPING = {"AMDAggressiveTestStrategy": AMDOpenAggressiveTestingStrategyCreateBot,
                "ExperimentalBotStrategy": AMDExperiment,
                "AMDOpenAggressiveTestingStrategyCreateBotV2": AMDOpenAggressiveTestingStrategyCreateBotV2}

BOTS_OFFLINE_MAPPING = {"AMDAggressiveTestStrategy": AMDOpenAggressiveOfflineTestingStrategyCreateBot,
                        "ExperimentalBotStrategy": AMDExperiment}

STOCKS = ["TWTR", "MSFT", "GM", "AAL", "AMD", "AAPL", "FB", "PFE", "UAL", "CSCO", 
                  "BAC", "DIS", "CRM", "BABA", "CMCSA", "PYPL", "ORCL", "NVDA", "GILD", "C", 
                  "INTC", "MRVL", "MDLZ", "BA", "V", "JPM"]