from flask import Flask, request, jsonify
import logging

from FootBotApi.calculator import build_stats, OutputTeamStats
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
    items = fetch_flat_matches(before_date, league_id, team_id)
    return jsonify(items.to_json())


@app.route("/api/v1/stats/<int:league_id>/<int:team_id>/<before_date>", methods=['GET'])
def get_stats(league_id, team_id, before_date):
    items = fetch_flat_matches(before_date, league_id, team_id)
    output = OutputTeamStats()
    build_stats(items, team_id , league_id, before_date, output)
    return output.toJSON()


def fetch_flat_matches(before_date, league_id, team_id):
    connect(database_name, host=server_name, port=port)
    items = flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                                & Q(league_id=league_id) & Q(time_starting_at_date__lte=before_date)).order_by(
        'time_starting_at_date-')[:1]
    return items


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
