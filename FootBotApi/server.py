import mongoengine
import pymongo
from flask import Flask, jsonify
from flask.blueprints import Blueprint
from FootBotApi.calculator.ComputedFromEventsFields import ComputedFromEventsFields
from FootBotApi.calculator.ComputedFromEventsFields import minutes
from FootBotApi.calculator.calculator import build_computed_stats, build_historical_stats, OutputTeamStats
from FootBotApi.config import configure_app
from FootBotApi.fetcher.fetcher import fetch_match, fetch_flat_match, fetch_flat_matches
from FootBotApi.logger.logger import log_error
from flasgger import Swagger
from flasgger import swag_from

bp = Blueprint(__name__.split('.')[0], __name__.split('.')[0])


def create_app():
    the_app = Flask(__name__.split('.')[0], instance_relative_config=True)
    configure_app(the_app)
    swagger = Swagger(the_app)
    the_app.register_blueprint(bp)
    return the_app


@swag_from('historical-stats.yml')
@bp.route("/api/v1/flat-matches/<int:league_id>/<int:team_id>/<before_date>/<time_status>/historical-stats",
          methods=['GET'])
def get_historical_stats(league_id, team_id, before_date, time_status):
    output = OutputTeamStats()
    try:
        items = fetch_flat_matches(before_date, league_id, team_id, time_status)

    except pymongo.errors.ServerSelectionTimeoutError as sste:
        log_error(sste, 'historical-stats', team_id)
        raise pymongo.errors.ServerSelectionTimeoutError from sste
    except mongoengine.connection.ConnectionFailure as cf:
        log_error(cf, 'historical-stats', team_id)
        raise mongoengine.connection.ConnectionFailure from cf

    try:
        build_historical_stats(items, team_id, league_id, before_date, output)
    except mongoengine.errors.FieldDoesNotExist as fdne:
        log_error(fdne, 'computed-stats', team_id)
    finally:
        return jsonify(output.toJSON())


@swag_from('computed-stats.yml')
@bp.route("/api/v1/flat-matches/<int:match_id>/<time_status>/computed-stats", methods=['GET'])
def get_computed_stats(match_id, time_status):
    output = OutputTeamStats()
    the_matches = {}
    try:
        the_matches = fetch_flat_match(match_id, time_status)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        log_error(sste, 'computed-stats', match_id)
        raise pymongo.errors.ServerSelectionTimeoutError from sste
    except mongoengine.connection.ConnectionFailure as cf:
        log_error(cf, 'computed-stats', match_id)
        raise mongoengine.connection.ConnectionFailure from cf
    try:
        for m in the_matches:
            build_computed_stats(m, output)
    except mongoengine.errors.FieldDoesNotExist as fdne:
        log_error(fdne, 'computed-stats', match_id)
    finally:
        return jsonify(output.toJSON())


@bp.route("/api/v1/matches/<int:match_id>/<time_status>/event-stats", methods=['GET'])
def get_match(match_id, time_status):
    output = OutputTeamStats()
    the_matches = {}
    try:
        the_matches = fetch_match(match_id, time_status)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        log_error(sste, 'event-stats', match_id)
        raise pymongo.errors.ServerSelectionTimeoutError from sste
    except mongoengine.connection.ConnectionFailure as cf:
        log_error(cf, 'event-stats', match_id)
        raise mongoengine.connection.ConnectionFailure from cf

    try:
        for m in the_matches:
            afef = ComputedFromEventsFields(m.events['data'], match_id, m.localteam_id, m.visitorteam_id, minutes)
            afef.init_output_dictionaries()
            afef.compute_output_values_from_events()
            afef.add_output_values_to_object(output)
        return jsonify(output.toJSON())
    except mongoengine.errors.FieldDoesNotExist as fdne:
        log_error(fdne, 'stats', match_id)
    finally:
        return jsonify(output.toJSON())


@bp.route("/api/v1/flat-matches/<int:league_id>/<int:team_id>/<before_date>/<time_status>", methods=['GET'])
def get_flat_matches(league_id, team_id, before_date, time_status):
    try:
        items = fetch_flat_matches(before_date, league_id, team_id, time_status)
    except pymongo.errors.ServerSelectionTimeoutError as sste:
        log_error(sste, 'flat-matches', team_id)
        raise pymongo.errors.ServerSelectionTimeoutError from sste
    except mongoengine.connection.ConnectionFailure as cf:
        log_error(cf, 'flat-matches', team_id)
        raise mongoengine.connection.ConnectionFailure from cf
    finally:
        return jsonify(items.to_json())


@bp.app_errorhandler(pymongo.errors.ServerSelectionTimeoutError)
def handle_error(error):
    message = [str(x) for x in error.args]
    status_code = 500
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), status_code


if __name__ == '__main__':
    create_app().run()
