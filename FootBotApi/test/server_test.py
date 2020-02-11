import mock
import pytest
from FootBotApi.models import flatmatches
from FootBotApi.server import create_app
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


def test_get(mock_get_value, test_client):
    response = test_client.get('/api/v1/stats/72/629/2020-01-20/FT')
    assert response.status_code == 200
    data_json2 = json.loads(response.get_json(silent=True, force=True))
    assert data_json2['league_id'] == 72
    #   response2 = test_client.get('/api/v1/matches/72/629/2020-01-20/FT')
    #  data_json3 = json.loads(response2.get_json(silent=True, force=True))
    # assert data_json3['league_id'] == 72
    # assert p[0:30] == 72
    #    assert json.loads(response.get_data())['team_id'] == 629
