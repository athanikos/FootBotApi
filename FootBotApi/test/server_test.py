import mock
import pytest
from FootBotApi.models import flatmatches, matches, Event, Time
from FootBotApi.server import create_app
from FootBotApi.fetcher.fetcher import do_connect
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


def test_historical_stats_uri(mock_fetch_flat_matches, test_client):
    response = test_client.get('/api/v1/flat-matches/72/629/2020-01-20/FT/historical-stats')
    assert response.status_code == 200
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert data_json2['league_id'] == 72
    assert data_json2['team_id'] == 629


def test_get_computed_stats(test_client):
    do_connect()
    flatmatches.objects.all().delete()
    the_match = flatmatches()
    the_match.match_id = 2
    the_match.time_status = 'FT'
    the_match.stats_data_0_goals = 1
    the_match.stats_data_1_goals = 0
    the_match.save(force_insert=True ,validate = False,clean=False)
    response = test_client.get('/api/v1/flat-matches/2/FT/computed-stats')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert data_json2['home_points'] == 3
    assert data_json2['away_points'] == 0


def test_get_computed_stats_when_field_values_are_none(test_client):
    do_connect()
    flatmatches.objects.all().delete()
    the_match = flatmatches()
    the_match.match_id = 2
    the_match.time_status = 'FT'
    the_match.stats_data_1_goals = 0
    the_match.save(force_insert=True ,validate = False,clean=False)
    response = test_client.get('/api/v1/flat-matches/2/FT/computed-stats')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert 'home_points' not in data_json2
    assert 'away_points' not in data_json2

def test_get_flat_matches(test_client):
    do_connect()
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
    response = test_client.get('/api/v1/flat-matches/3/1/2020-01-21/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert len(data_json2) == 1

    response = test_client.get('/api/v1/flat-matches/3/1/2020-01-20/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert len(data_json2) == 0

    response = test_client.get('/api/v1/flat-matches/3/1/2020-01-19/FT')
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert response.status_code == 200
    assert len(data_json2) == 0