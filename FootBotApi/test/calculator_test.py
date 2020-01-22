import pytest
from FootBotApi.models import *
from FootBotApi.calculator import *

from FootBotApi.test.helpers import get_match


def test_compute_average_variable_not_in_place():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    in_out_pairs = {"stats_data_0_goals": 'out', "stats_data_1_goals": 'out2'}

    object_to_set = JsonSerializable()
    with pytest.raises(NameError):
        compute_average(matches, 1, in_out_pairs, object_to_set)


def test_compute_average():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    matches.append(match2)
    object_to_set = JsonSerializable()

    in_out_pairs = {"stats_data_0_goals": 'out', "stats_data_1_goals": 'out2'}
    compute_average(matches, 1, in_out_pairs, object_to_set)
    assert object_to_set.out == 1
    assert object_to_set.out2 == .5



