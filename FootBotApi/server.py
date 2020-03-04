from flask import Flask, jsonify, Blueprint
from keyring import get_password

from FootBotApi.calculator.ComputedFromEventsFields import ComputedFromEventsFields, minutes
from FootBotApi.calculator.calculator import build_historical_stats, OutputTeamStats, build_computed_stats
from FootBotApi.models import flatmatches, matches
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from FootBotApi.config import configure_app
from flask import current_app as app
import keyring
bp = Blueprint('myapp', __name__)


def create_app():
    the_app = Flask(__name__, instance_relative_config=True)
    configure_app(the_app)
    the_app.register_blueprint(bp)
    return the_app


@bp.route("/api/v1/flat-matches/<int:league_id>/<int:team_id>/<before_date>/<time_status>/historical-stats", methods=['GET'])
def get_historical_stats(league_id, team_id, before_date, time_status):
    items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    output = OutputTeamStats()
    build_historical_stats(items, team_id, league_id, before_date, output)
    return jsonify(output.toJSON())


@bp.route("/api/v1/flat-matches/<int:match_id>/<time_status>/computed-stats", methods=['GET'])
def get_computed_stats(match_id, time_status):
    the_matches = fetch_flat_match(match_id, time_status)
    output = OutputTeamStats()
    for m in the_matches:
        build_computed_stats(m,output)
    return jsonify(output.toJSON())


@bp.route("/api/v1/matches/<int:match_id>/<time_status>/event-stats", methods=['GET'])
def get_match(match_id, time_status):
    the_matches = fetch_match(match_id, time_status)
    output = OutputTeamStats()
    for m in the_matches:
        afef = ComputedFromEventsFields(m.events['data'], match_id, m.localteam_id, m.visitorteam_id, minutes)
        afef.init_output_dictionaries()
        afef.compute_output_values_from_events()
        afef.add_output_values_to_object(output)
    return jsonify(output.toJSON())


@bp.route("/api/v1/flat-matches/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_flat_matches(league_id, team_id, before_date, time_status):
    items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    return jsonify(items.to_json())


def fetch_flat_matches(before_date, league_id, team_id, time_status):
    do_connect()
    return flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                               & (Q(time_status=time_status))
                               & Q(league_id=league_id) & Q(time_starting_at_date__lt=before_date)).order_by(
        'time_starting_at_date-')[:10]


def fetch_match(the_match_id, time_status):
    do_connect()
    return matches.objects((Q(match_id=the_match_id) & Q(time__status=time_status)))


def fetch_flat_match(the_match_id, time_status):
    do_connect()
    return flatmatches.objects((Q(match_id=the_match_id) & Q(time_status=time_status)))


def do_connect():
    url = 'mongodb://foot:' + get_password('FootBotApi', 'foot') + '@' + app.config['SERVERNAME'] + ':' + str(app.config['PORT']) + '/' + app.config['DATABASE']
    connect( db=app.config['DATABASE'], username='foot', password=get_password('FootBotApi', 'foot'), host=url)

if __name__ == '__main__':
    bp.run()
