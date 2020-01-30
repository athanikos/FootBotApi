import pytest

from FootBotApi.calculator.VariablePair import VariablePair, Calculation_Method
from FootBotApi.calculator.calculator import OutputTeamStats, compute_average, init_value, build_stats, SUM, get_value
from FootBotApi.test.helpers import get_match


def test_compute_average_variable_not_in_place():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    in_out_pairs = {"stats_data_0_goals": 'out', "dummy": 'out2'}

    object_to_set = OutputTeamStats()
    with pytest.raises(NameError):
        compute_average(matches, 1, in_out_pairs, object_to_set)


def test_compute_average():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    matches.append(match2)
    object_to_set = OutputTeamStats()
    in_out_pairs = {"stats_data_0_goals": 'out', "stats_data_1_goals": 'out2'}
    compute_average(matches, 1, in_out_pairs, object_to_set)
    assert object_to_set.out == 1
    assert object_to_set.out2 == .5


def increment_average_value(in_out_pairs, param, object_to_set, param1):
    pass


def test_increment_average_value():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    matches.append(match1)
    object_to_set = OutputTeamStats()
    in_out_pairs = {"stats_data_0_goals": 'out'}
    init_value(in_out_pairs, "stats_data_0_goals", object_to_set, SUM)
    increment_average_value(in_out_pairs, "stats_data_0_goals", object_to_set, None)
    assert getattr(object_to_set, "out" + SUM) == 0


def test_build_stats():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    matches.append(match1)
    object_to_set = OutputTeamStats()
    variable_pairs =[]
    variable = VariablePair(1, 1, 1,  'stats_data_0_goals', 'out', Calculation_Method.AVG)
    variable_pairs.append(variable)
    build_stats(matches, 1, 1, "1/1/2010", object_to_set)
    assert getattr(object_to_set, "team_id") == 1
    assert getattr(object_to_set, "league_id") == 2
    assert getattr(object_to_set, "before_date") == '2011-01-01'


def test_get_value():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match2 = get_match(1, 1, 2, 1, 1)
    matches.append(match1)
    matches.append(match2)
    object_to_set = OutputTeamStats()
    in_out_pairs = {"stats_data_0_goals": 'out', "stats_data_1_goals": 'out2'}
    assert get_value(in_out_pairs, "stats_data_0_goals", object_to_set) == 0
    assert get_value(in_out_pairs, "dont exists", object_to_set) == 0


def test_equals():
    expr = "1==1"
    assert eval(expr) == True


def test_eval_with_object():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    match1.league_id = 69
    match1.localteam_id = 32
    isAway = match1.localteam_id == 32
    assert eval("match1.league_id==69") == True
    isHome =  eval(" match1.localteam_id == 32 ")
    assert isHome == True


