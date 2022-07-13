import flask
from BacktestingAPI.strategies.strategies import strategies
from BacktestingAPI.backtest.backtest import backtest
from BacktestingAPI.template.template import template
from BacktestingAPI.csv.csv import csv
from flask_cors import CORS

START_ROUTE = '/v1/'

tasks = {}

app = flask.Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.register_blueprint(strategies, url_prefix=f'{START_ROUTE}/strategies')
app.register_blueprint(backtest, url_prefix=f'{START_ROUTE}/backtest')
app.register_blueprint(template, url_prefix=f'{START_ROUTE}/backtest/template')
app.register_blueprint(csv, url_prefix=f'{START_ROUTE}/csv')