from flask import Flask, request, jsonify
import logging

from FootBotApi.calculator import compute_average
from FootBotApi.models import flatmatches
from mongoengine import connect
from mongoengine.queryset.visitor import Q

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
server_name = "localhost"
port = 27017
database_name = "book"


@app.route('/')
def hello_world():
    return 'Hello from FootBot Api !'


@app.route("/api/v1/matches/<int:league_id>/<int:team_id>/<before_date>", methods=['GET'])
def get_flat_matches(league_id, team_id, before_date):
    connect(database_name, host=server_name, port=port)
    items = flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                                & Q(league_id=league_id) & Q(time_starting_at_date__lte=before_date)).order_by('time_starting_at_date-')[:10]

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
