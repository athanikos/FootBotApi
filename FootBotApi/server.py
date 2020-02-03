from flask import Flask, jsonify, Blueprint
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


@bp.route("/api/v1/matches", methods=['GET'])
def get_matches():
    items = fetch_matches()
    return jsonify(items.to_json())


def fetch_flat_matches(before_date, league_id, team_id, time_status):
    connect(app.config['DATABASE'], host=app.config['SERVERNAME'], port=app.config['PORT'])
    return flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                               & (Q(time_status=time_status))
                               & Q(league_id=league_id) & Q(time_starting_at_date__lte=before_date)).order_by(
        'time_starting_at_date-')[:10]


def fetch_matches():
    connect(app.config['DATABASE'], host=app.config['SERVERNAME'], port=app.config['PORT'])
    test = matches.objects(Q(id=11888482))[80:81]

    for t in test:
        print(t.id)
        for e in t.events:
            print(e)
            print(len(t.events))
            print(t.events['data'][0].team_id)
            for item in t.events['data']:
                print(item.minute)

    return test


if __name__ == '__main__':
    bp.run()
