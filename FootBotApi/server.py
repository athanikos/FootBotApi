import flask
from flask import Flask, request, jsonify, Blueprint
import logging

from FootBotApi.calculator.calculator import build_stats, OutputTeamStats
from FootBotApi.models import flatmatches
from mongoengine import connect
from mongoengine.queryset.visitor import Q

server_name = "localhost"
port = 27017
database_name = "book"


def create_app(config_filename='flask.cfg'):
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(bp)
    app.config.from_pyfile(config_filename)
    return app


logging.basicConfig(level=logging.DEBUG)
bp = Blueprint('myapp', __name__)
create_app('flask.cfg')


@bp.route('/')
def hello_world():
    return 'Hello from FootBot Api !'


@bp.route("/api/v1/matches/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_flat_matches(league_id, team_id, before_date, time_status):
    items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    return jsonify(items.to_json())


@bp.route("/api/v1/stats/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_stats(league_id, team_id, before_date, time_status):
    items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    output = OutputTeamStats()
    build_stats(items, team_id, league_id, before_date, output)
    return output.toJSON()


def fetch_flat_matches(before_date, league_id, team_id, time_status):
    connect(database_name, host=server_name, port=port)
    items = flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                                & (Q(time_status=time_status) )
                                & Q(league_id=league_id) & Q(time_starting_at_date__lte=before_date)).order_by(
        'time_starting_at_date-')[:10]
    return items


@bp.before_request
def before():
    pass


@bp.after_request
def after(response):
    return response


if __name__ == '__main__':
    bp.run()
