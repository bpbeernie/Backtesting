import flask
from BacktestingAPI.strategies.strategies import strategies
from BacktestingAPI.backtest.backtest import backtest
from BacktestingAPI.template.template import template

START_ROUTE = '/v1/'

tasks = {}

app = flask.Flask(__name__)
app.register_blueprint(strategies, url_prefix=f'{START_ROUTE}/strategies')
app.register_blueprint(backtest, url_prefix=f'{START_ROUTE}/backtest')
app.register_blueprint(template, url_prefix=f'{START_ROUTE}/backtest/template')

app.run()