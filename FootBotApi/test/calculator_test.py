import pytest

from FootBotApi.models import *
from FootBotApi.calculator import *


def test_compute_average_goals():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    matches.append(match2)
    assert compute_average_goals(matches, 1) == 1
    assert compute_average_goals(matches, 2) == .5
    matches = []
    assert compute_average_goals(matches, 1) == 0

def test_compute_average_variable_not_in_place():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    with pytest.raises(NameError):
        compute_average(matches, 1, 'i_dont_exist')


def test_compute_average():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    matches.append(match2)
    assert compute_average(matches, 1, 'stats_data_0_goals') == 1
    assert compute_average(matches, 1, 'stats_data_1_goals') == .5


def get_match(league_id, localteam_id, visitorteam_id, stats_data_0_goals, stats_data_1_goals):
    match = flatmatches()
    match.league_id = league_id
    match.localteam_id = localteam_id
    match.visitorteam_id = visitorteam_id
    match.stats_data_0_goals = stats_data_0_goals
    match.stats_data_1_goals = stats_data_1_goals
    return match
