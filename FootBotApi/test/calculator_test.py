import pytest

from FootBotApi.calculator.CalculatedField import CalculatedField, Calculation_Method, Include
from FootBotApi.calculator.calculator import OutputTeamStats, compute_average, build_stats, SUM
from FootBotApi.test.helpers import get_match


def test_build_stats():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    matches.append(match1)
    object_to_set = OutputTeamStats()
    variable_pairs =[]
    variable = CalculatedField(1, 'stats_data_0_goals', 'out', Calculation_Method.AVG, Include.ALL)
    variable_pairs.append(variable)
    build_stats(matches, 1, 1, "1/1/2010", object_to_set)
    assert getattr(object_to_set, "team_id") == 1
    assert getattr(object_to_set, "league_id") == 1
    assert getattr(object_to_set, "before_date") == "1/1/2010"


def test_CalculatedVariable_calculate():
     variable =  CalculatedField(1, 'stats_data_0_goals', 'out', Calculation_Method.AVG, Include.HOME)
     matches = []
     match1 = get_match(1, 1, 2, 3, 0)
     match2 = get_match(1, 3, 2, 2, 0)
     matches.append(match1)
     matches.append(match2)
     variable.calculate(matches)
     assert variable.sum == 3
     assert variable.count == 1


