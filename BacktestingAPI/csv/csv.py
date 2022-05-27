import flask
import BacktestingAPI.services.mergeCSVService as mergeCSVService
import BacktestingAPI.services.archiveCSVService as archiveCSVService


csv = flask.Blueprint("csv", __name__)

@csv.route('/merge', methods=['POST'])
def merge_csv():
    mergeCSVService.mergeCSV()

    return "Complete", 200, {'ContentType':'application/json'} 


@csv.route('/archive', methods=['POST'])
def archive_csv():
    archiveCSVService.archive()

    return "Complete", 200, {'ContentType':'application/json'} 