import pytest

from FootBotApi.calculator.CalculatedVariable import CalculatedVariable, Calculation_Method
from FootBotApi.calculator.calculator import OutputTeamStats, compute_average, init_value, build_stats, SUM, get_value
from FootBotApi.test.helpers import get_match

def test_build_stats():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    matches.append(match1)
    object_to_set = OutputTeamStats()
    variable_pairs =[]
    variable = CalculatedVariable(1, 1, 1, 'stats_data_0_goals', 'out', Calculation_Method.AVG)
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


