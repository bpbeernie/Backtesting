import flask
import json
import time
import BacktestingAPI.runTest as runTest
import uuid
from AMDOpenAggressiveTestingStrategy import Settings as settings
from threading import Thread
from datetime import datetime
from IB import IBClient as ibClient
import Globals.Strategies as strategies 
import IB.Constants as ibConsts

app = flask.Flask(__name__)

DATE_FORMAT = '%b %d %Y %I:%M%p'
START_ROUTE = '/v1/'
ib = None
tasks = {}

def run_loop(ib):
    ib.run()

def setup():
    global ib

    ib = ibClient.IBApi()
    ib.connect(ibConsts.LOCALIP, ibConsts.PORT, 1)
    ib_thread = Thread(target=run_loop, args=(ib,), daemon=True)
    ib_thread.start()
    time.sleep(1)


@app.route(START_ROUTE + '/strategies', methods=['GET'])
def get_strategies():
    strategy_list = list(strategies.strategy_mapping.keys())
    
    return flask.jsonify(strategy_list)


def parse_date_range(date_range):
    parse_date_range = []
    
    for single_range in date_range:
        parse_date_range.append((single_range[0], datetime.strptime(single_range[1], DATE_FORMAT), datetime.strptime(single_range[2], DATE_FORMAT)))
        
    return parse_date_range

def parse_strategy_list(strategy_list):
    parse_strategy_list = []
    
    for strategy in strategy_list:
        parse_strategy_list.append(strategies.strategy_mapping[strategy])
        
    return parse_strategy_list

@app.route(START_ROUTE + '/backtest', methods=['POST'])
def create_backtest():
    global ib
    global tasks
    date_range = parse_date_range(flask.request.json['DateRange'])
    stock_list = flask.request.json['Stocks']
    strategy_list = parse_strategy_list(flask.request.json['Strategies'])

    settings.DATE_RANGE = date_range
    settings.STOCKS_TO_TEST = stock_list
    settings.STRATEGY_LIST = strategy_list
    
    taskID = str(uuid.uuid4())
    t = Thread(target=runTest.run, args=(ib,))
    t.start()
    tasks[taskID] = t
    
    return json.dumps({'ID':taskID}), 200, {'ContentType':'application/json'} 

@app.route(START_ROUTE + '/backtest/<taskID>', methods=['GET'])
def get_backtest(taskID):
    global tasks

    task = tasks[taskID]
    if task.is_alive():
        msg = f"Task {taskID} is still running!"
    else:
        msg = f"Task {taskID} is done!"
    
    return json.dumps({'Status': msg}), 200, {'ContentType':'application/json'} 

def stringfy_date_range(date_range):
    string_date_range = []
    for single_range in date_range:
        string_date_range.append((single_range[0], f'{single_range[1]:%b %d %Y %I:%M%p}', f'{single_range[2]:%b %d %Y %I:%M%p}'))
    
    return string_date_range

def create_backtest_response(date_range, stock_list, strategy_list):
    return {"DateRange": stringfy_date_range(date_range), "Stocks": stock_list, "Strategies": list(strategy_list)}

@app.route(START_ROUTE + '/backtest/template', methods=['GET'])
def get_backtest_template():
    date_range = settings.monthToDate()
    strategy_list = strategies.strategy_mapping.keys()
    
    return create_backtest_response(date_range, settings.STOCKS_TO_TEST, strategy_list)

@app.route(START_ROUTE + '/backtest/template/<year>', methods=['GET'])
def get_backtest_template_by_year(year):
    date_range = settings.monthsInYear(int(year))
    strategy_list = strategies.strategy_mapping.keys()
    print(strategy_list)
    
    return create_backtest_response(date_range, settings.STOCKS_TO_TEST, strategy_list)

setup()
app.run()