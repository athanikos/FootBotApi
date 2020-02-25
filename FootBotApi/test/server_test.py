import mock
import pytest
from FootBotApi.models import flatmatches, matches, Event, Time
from FootBotApi.server import create_app, connect
from flask import current_app as app
import json


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()


@pytest.fixture
def mock_fetch_flat_matches():
    with mock.patch(
            "FootBotApi.server.fetch_flat_matches",
            autospec=True,
    ) as _mock:
        ft = flatmatches()
        ft.league_id = -1
        yield ft


@pytest.fixture
def mock_fetch_match():
    e = Event()
    e.type = "goal"
    e.minute = 12
    e.team_id = 1
    e2 = Event()
    e2.type = "goal"
    e2.minute = 43
    e2.team_id = 1
    items = []
    m = matches()
    m.localteam_id = 1
    m.visitorteam_id = 2
    m.events = ({'data': [e,e2] } )
    m.league_id = -1
    with mock.patch(
            "FootBotApi.server.fetch_match",
            autospec=True,
            return_value= [m]
    ) as _mock2:
        yield [m]


def test_stats_uri(mock_fetch_flat_matches, test_client):
    response = test_client.get('/api/v1/stats/72/629/2020-01-20/FT')
    assert response.status_code == 200
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert data_json2['league_id'] == 72
    assert data_json2['team_id'] == 629

    
def test_matches_uri(mock_fetch_match, test_client):
    response = test_client.get('/api/v1/matches/72/FT')
    assert response.status_code == 200
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert data_json2['HOME_TEAM_GOALS_UP_TO_14'] == 1


def test_get_match(test_client):
    connect(app.config['DATABASE'], host=app.config['SERVERNAME'], port=app.config['PORT'])
    matches.objects.all().delete()
    the_match = matches()
    the_match.visitorteam_id = 999
    the_match.localteam_id = 6666
    the_match.match_id = 2
    the_time = Time()
    the_time.status = 'FT'
    the_match.time = the_time
    the_event = Event()
    the_event.minute = 11
    the_event.team_id = 999
    the_event.type ='goal'
    the_match.events = { 'data' : [ the_event ] }
    the_match.save(force_insert=True ,validate = False,clean=False)
    response = test_client.get('/api/v1/matches/2/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert data_json2['home_team_id'] == 6666


def test_get_flat_matches(test_client):
    connect(app.config['DATABASE'], host=app.config['SERVERNAME'], port=app.config['PORT'])
    flatmatches.objects.all().delete()
    flat_match1 = flatmatches()
    flat_match1.localteam_id = 1
    flat_match1.visitorteam_id =2
    flat_match1.league_id = 3
    flat_match1.time_status = 'FT'
    flat_match1.time_starting_at_date = "2020-01-20"
    flat_match2 = flatmatches()
    flat_match2.localteam_id = 4
    flat_match2.visitorteam_id = 2
    flat_match2.league_id = 3
    flat_match2.time_status = 'FT'
    flat_match2.time_starting_at_date = "2020-01-20"

    flat_match1.save(force_insert=True ,validate = False,clean=False)
    response = test_client.get('/api/v1/flatmatches/3/1/2020-01-21/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert len(data_json2) == 1

    response = test_client.get('/api/v1/flatmatches/3/1/2020-01-20/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert len(data_json2) == 0

    response = test_client.get('/api/v1/flatmatches/3/1/2020-01-19/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert len(data_json2) == 0