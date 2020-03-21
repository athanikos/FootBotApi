from mongoengine import connect, Q
from flask import current_app as app
from FootBotApi.models import flatmatches, matches, leagues


def fetch_flat_matches(before_date, league_id, team_id, time_status):
    do_connect()
    return flatmatches.objects((Q(localteam_id=team_id) | Q(visitorteam_id=team_id))
                               & (Q(time_status=time_status))
                               & Q(league_id=league_id) & Q(time_starting_at_date__lt=before_date)).order_by(
        'time_starting_at_date-')[:10]


def fetch_leagues(league_id):
    do_connect()
    if league_id is None:
        return leagues.objects()
    print(league_id)
    return leagues.objects((Q(league_id=league_id)))


def fetch_match(the_match_id, time_status):
    do_connect()
    return matches.objects((Q(match_id=the_match_id) & Q(time__status=time_status)))


def fetch_flat_match(the_match_id, time_status):
    do_connect()
    return flatmatches.objects((Q(match_id=the_match_id) & Q(time_status=time_status)))


def do_connect():
    url = 'mongodb://' + app.config['USERNAME'] + ':' + app.config['PASSWORD'] + '@' + app.config[
        'SERVERNAME'] + ':' + str(app.config['PORT']) + '/?authSource=admin'
    conn = connect(db=app.config['DATABASE'], username=app.config['USERNAME'], host=url)

