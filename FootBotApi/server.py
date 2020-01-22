
from flask import Flask, request, jsonify
import logging
from FootBotApi.models import flatmatches
from mongoengine import connect

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
server_name = "localhost"
port = "27017"
database_name = "book"

@app.route('/')
def hello_world():
    return 'Hello Predictions!'

@app.route("/api/v1/matches/<int:league_id>/<int:team_id>/<before_date>", methods=['GET'])
def get_flat_matches(league_id, team_id, before_date):
    connect('book', host='localhost', port=27017)
    items = flatmatches.objects(localteam_id=team_id, league_id=league_id).order_by('time_starting_at_date-')
    return jsonify(items.to_json())
    return jsonify({'message': 'not found'})


@app.before_request
def before():
    app.logger.info(request.headers)
    app.logger.info(request.data)
    pass


@app.after_request
def after(response):
    app.logger.info(response.status)
    app.logger.info(response.headers)
    app.logger.info(response.get_data())
    return response


if __name__ == '__main__':
    app.run()
