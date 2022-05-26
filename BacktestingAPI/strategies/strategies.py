import flask
from Globals.Bots import BOTS_MAPPING

strategies = flask.Blueprint("strategies", __name__)

@strategies.route('/', methods=['GET'])
def get_strategies():
    strategies = list(BOTS_MAPPING.keys())
    
    return flask.jsonify(strategies)


