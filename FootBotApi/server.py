import json

from flask import Flask, jsonify, Blueprint
from FootBotApi.calculator.AggregatedFromEventsFields import AggregatedFromEventsFields, minutes
from FootBotApi.calculator.calculator import build_stats, OutputTeamStats
from FootBotApi.models import flatmatches, matches
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from FootBotApi.config import configure_app
from flask import current_app as app

bp = Blueprint('myapp', __name__)


def create_app():
    the_app = Flask(__name__, instance_relative_config=True)
    configure_app(the_app)
    the_app.register_blueprint(bp)
    return the_app


@bp.route("/api/v1/flatmatches/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_flat_matches(league_id, team_id, before_date, time_status):
    items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    return jsonify(items.to_json())


@bp.route("/api/v1/stats/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_stats(league_id, team_id, before_date, time_status):
    items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    output = OutputTeamStats()
    build_stats(items, team_id, league_id, before_date, output)
    return jsonify(output.toJSON())


@bp.route("/api/v1/matches/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_matches(league_id, team_id, before_date, time_status):
    output_items = []
    the_matches = fetch_matches(league_id,team_id,before_date,time_status)
    output = OutputTeamStats()
    output_items.append(output.toJSON())
    for m in the_matches:
        output = OutputTeamStats()
        afef = AggregatedFromEventsFields(m.events['data'],m.localteam_id,m.visitorteam_id,minutes)
        afef.init_output_dictionaries()
        afef.compute_output_values_from_events()
        afef.add_output_values_to_object(output)
        output_items.append(output.toJSON())
    return jsonify(json.dumps(output_items))


def fetch_flat_matches(before_date, league_id, team_id, time_status):
    connect(app.config['DATABASE'], host=app.config['SERVERNAME'], port=app.config['PORT'])
    return flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                               & (Q(time_status=time_status))
                               & Q(league_id=league_id) & Q(time_starting_at_date__lte=before_date)).order_by(
        'time_starting_at_date-')[:10]


def fetch_matches(league_id, team_id, before_date, time_status):
    connect(app.config['DATABASE'], host=app.config['SERVERNAME'], port=app.config['PORT'])
    return matches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
               &Q(league_id=league_id) ).order_by(
        'time.starting_at.date-')[:1]


if __name__ == '__main__':
    bp.run()
