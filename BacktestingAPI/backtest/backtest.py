import flask
from Strategies import Settings as settings
from Globals.Bots import BOTS_MAPPING, BOTS_OFFLINE_MAPPING
from IB import IBClient as ibClient
import IB.Constants as ibConsts
from threading import Thread
import time
from datetime import datetime
from BacktestingAPI.services import runTestService
import uuid
import json
import pprint

backtest = flask.Blueprint("backtest", __name__)
DATE_FORMAT = '%b %d %Y %I:%M%p'
ib = None
tasks = {}
initialized = False

def setup():
    global ib

    try:
        ib = ibClient.IBApi()
        ib.connect(ibConsts.LOCALIP, ibConsts.PORT, 1)
        ib_thread = Thread(target=run_loop, args=(ib,), daemon=True)
        ib_thread.start()
        time.sleep(1)
    except:
        print("Offline Mode!")

def run_loop(ib):
    ib.run()

def parse_date_range(date_range):
    parse_date_range = []
    
    for single_range in date_range:
        parse_date_range.append((single_range[0], datetime.strptime(single_range[1], DATE_FORMAT), datetime.strptime(single_range[2], DATE_FORMAT)))
        
    return parse_date_range

def parse_strategy_list(strategy_list):
    parse_strategy_list = []
    
    for strategy in strategy_list:
        parse_strategy_list.append(BOTS_MAPPING[strategy])
        
    return parse_strategy_list

def parse_strategy_list_offline(strategy_list):
    parse_strategy_list = []
    
    for strategy in strategy_list:
        parse_strategy_list.append(BOTS_OFFLINE_MAPPING[strategy])
        
    return parse_strategy_list

@backtest.route('/', methods=['POST'])
def create_backtest():
    global ib
    global tasks
    global initialized
    
    if not initialized:
        setup()
        initialized = True
    
    date_range = parse_date_range(flask.request.json['DateRange'])
    stock_list = flask.request.json['Stocks']
    strategy_list = parse_strategy_list(flask.request.json['Strategies'])

    settings.DATE_RANGE = date_range
    settings.STOCKS_TO_TEST = stock_list
    settings.STRATEGY_LIST = strategy_list
    
    taskID = str(uuid.uuid4())
    t = Thread(target=runTestService.run, args=(ib,))
    t.start()
    tasks[taskID] = t
    
    return json.dumps({'ID':taskID}), 200, {'ContentType':'application/json'} 

@backtest.route('/offline', methods=['POST'])
def create_offline_backtest():
    global tasks
    
    date_range = parse_date_range(flask.request.json['DateRange'])
    stock_list = flask.request.json['Stocks']
    strategy_list = parse_strategy_list_offline(flask.request.json['Strategies'])

    settings.DATE_RANGE = date_range
    settings.STOCKS_TO_TEST = stock_list
    settings.STRATEGY_LIST = strategy_list
    
    pprint.pprint(settings.DATE_RANGE)
    
    taskID = str(uuid.uuid4())
    t = Thread(target=runTestService.run, args=(None,))
    t.start()
    tasks[taskID] = t
    
    return json.dumps({'ID':taskID}), 200, {'ContentType':'application/json'} 

@backtest.route('/<taskID>', methods=['GET'])
def get_backtest(taskID):
    global tasks

    task = tasks[taskID]
    if task.is_alive():
        msg = f"Task {taskID} is still running!"
    else:
        msg = f"Task {taskID} is done!"
    
    return json.dumps({'Status': msg}), 200, {'ContentType':'application/json'} 