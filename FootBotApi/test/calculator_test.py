import pytest
from FootBotApi.models import *
from FootBotApi.calculator import *

from FootBotApi.test.helpers import get_match


def test_compute_average_variable_not_in_place():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    with pytest.raises(NameError):
        compute_average(matches, 1, 'i_dont_exist', 'dummy')


def test_compute_average():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    matches.append(match2)
    assert compute_average(matches, 1, 'stats_data_0_goals', 'out').out == 1
    assert compute_average(matches, 1, 'stats_data_1_goals', 'out2').out2 == .5


