from AMDOpenAggressiveTestingStrategy.TestStrategyBotBuilder import create_bots as AMDOpenAggressiveTestingStrategyCreateBot, create_bots_offline as AMDOpenAggressiveOfflineTestingStrategyCreateBot
from AMDOpenAggressiveExperimentalTestingStrategy.TestStrategyExperimentalBotBuilder import create_bots_offline as AMDExperiment

BOTS_MAPPING = {"AMDAggressiveTestStrategy": AMDOpenAggressiveTestingStrategyCreateBot,
                "ExperimentalBotStrategy": AMDExperiment}

BOTS_OFFLINE_MAPPING = {"AMDAggressiveTestStrategy": AMDOpenAggressiveOfflineTestingStrategyCreateBot,
                        "ExperimentalBotStrategy": AMDExperiment}