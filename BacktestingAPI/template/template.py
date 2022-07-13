import flask
from Globals.Bots import BOTS_MAPPING
import settings
from Globals import Constants as consts

template = flask.Blueprint("template", __name__)

def create_backtest_response(date_range, stock_list, strategy_list):
    return {"DateRange": stringfy_date_range(date_range), "Stocks": stock_list, "Strategies": list(strategy_list)}

def stringfy_date_range(date_range):
    string_date_range = []
    for single_range in date_range:
        string_date_range.append((single_range[0], f'{single_range[1]:%b %d %Y %I:%M%p}', f'{single_range[2]:%b %d %Y %I:%M%p}'))
    
    return string_date_range

@template.route('', methods=['GET'])
def get_backtest_template():
    date_range = settings.monthToDate()
    strategy_list = BOTS_MAPPING.keys()
    
    return create_backtest_response(date_range, consts.STOCKS, strategy_list)

@template.route('/<year>', methods=['GET'])
def get_backtest_template_by_year(year):
    date_range = settings.monthsInYear(int(year))
    strategy_list = BOTS_MAPPING.keys()
    print(strategy_list)
    
    return create_backtest_response(date_range, consts.STOCKS, strategy_list)
