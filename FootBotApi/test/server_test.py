import mock
import pytest
from FootBotApi.models import flatmatches, matches, Event
from FootBotApi.server import create_app, fetch_matches
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
def mock_get_value():
    with mock.patch(
            "FootBotApi.server.fetch_flat_matches",
            autospec=True,
    ) as _mock:
        ft = flatmatches()
        ft.league_id = -1
        yield ft


@pytest.fixture
def mock_get_value_2():
    with mock.patch(
            "FootBotApi.server.fetch_matches",
            autospec=True,
    ) as _mock2:
        e = Event()
        e.type = "goal"
        e.minute = 12
        e.team_id = 1
        e2 = Event()
        e2.type = "goal"
        e2.minute = 43
        e2.team_id = 1
        m = matches()
        m.localteam_id =1
        m.visitorteam_id=2
        m.events.append(e)
        m.events.append(e2)
        m.league_id = -1
        yield m


def test_get(mock_get_value, test_client):
    response = test_client.get('/api/v1/stats/72/629/2020-01-20/FT')
    assert response.status_code == 200
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert data_json2['league_id'] == 72


def test_get_2(mock_get_value_2, test_client):
    response = test_client.get('/api/v1/matches/72/629/2020-01-20/FT')
    assert response.status_code == 200
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    print(data_json2)
