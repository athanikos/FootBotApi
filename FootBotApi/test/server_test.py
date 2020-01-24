from types import MethodType

import mock
import pytest
from flask import jsonify
from FootBotApi.models import flatmatches
from FootBotApi.server import get_flat_matches, create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask.cfg')
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


def test_get_flat_matches(mock_get_value, test_client):
    response = test_client.get('/api/v1/stats/72/629/2020-01-20/FT')
    assert response.status_code == 200
   # assert json.loads(response.get_data())['league_id'] == 72
