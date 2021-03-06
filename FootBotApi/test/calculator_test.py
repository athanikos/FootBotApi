from FootBotApi.calculator.ComputedFromMatchesField import ComputedFromMatchesField
from FootBotApi.calculator.calculator import OutputTeamStats, compute_historical_fields, build_historical_stats, \
    build_computed_stats
from FootBotApi.test.helpers import get_match
from FootBotApi.calculator.ComputedFromMatchesField import  Include
from FootBotApi.calculator.CalculationMethod import  CalculationMethod


def test_build_stats():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    matches.append(match1)
    object_to_set = OutputTeamStats()
    variable_pairs =[]
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG,
                                        Include.ALL)
    variable_pairs.append(variable)
    build_historical_stats(matches, 1, 1, "1/1/2010", object_to_set)
    assert getattr(object_to_set, "team_id") == 1
    assert getattr(object_to_set, "league_id") == 1
    assert getattr(object_to_set, "before_date") == "1/1/2010"


def test_calculated_variable_calculate():
     variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG,
                                          Include.HOME)
     matches = []
     match1 = get_match(1, 1, 2, 3, 0)
     match2 = get_match(1, 3, 2, 2, 0)
     matches.append(match1)
     matches.append(match2)
     variable.calculate(matches)
     assert variable.sum == 3
     assert variable.count == 1
     assert variable.get_output_value() == 3


def test_calculated_variable_calculate_sum():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.SUM, Include.HOME)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 1, 2, 2, 0)
    matches.append(match1)
    matches.append(match2)
    variable.calculate(matches)
    assert variable.sum == 5
    assert variable.count == 2
    assert variable.get_output_value() == 5


def test_calculated_variable_calculate_sum_all():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.SUM, Include.ALL)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 1, 2, 2, 0)
    match3 = get_match(1, 2, 1, 0, 2)
    matches.append(match1)
    matches.append(match2)
    matches.append(match3)
    variable.calculate(matches)
    assert variable.sum == 7
    assert variable.count == 3
    assert variable.get_output_value() == 7


def test_calculated_variable_calculate_count_all():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.COUNT, Include.HOME)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 1, 2, 2, 0)
    match3 = get_match(1, 2, 1, 0, 2)
    matches.append(match1)
    matches.append(match2)
    matches.append(match3)
    variable.calculate(matches)
    assert variable.sum == 5
    assert variable.count == 2
    assert variable.get_output_value() == 2


def test_calculated_variable_calculate_away_avg():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG, Include.AWAY)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 2, 1, 1, 2)
    match3 = get_match(1, 2, 1, 0, 8)
    matches.append(match1)
    matches.append(match2)
    matches.append(match3)
    variable.calculate(matches)
    assert variable.sum == 10
    assert variable.count == 2
    assert variable.get_output_value() == 5


def test_calculated_variable_calculate_away_count():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.COUNT, Include.AWAY)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 2, 1, 1, 2)
    match3 = get_match(1, 2, 1, 0, 8)
    matches.append(match1)
    matches.append(match2)
    matches.append(match3)
    variable.calculate(matches)
    assert variable.sum == 10
    assert variable.count == 2
    assert variable.get_output_value() == 2


def test_calculated_variable_calculate_away_avg_zero():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG, Include.AWAY)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 2, 3, 1, 2)
    match3 = get_match(1, 2, 3, 0, 8)
    matches.append(match1)
    matches.append(match2)
    matches.append(match3)
    variable.calculate(matches)
    assert variable.sum == 0
    assert variable.count == 0
    assert variable.get_output_value() == 0


def test_calculated_variable_calculate_away_sum():
    variable = ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.SUM, Include.AWAY)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 2, 1, 1, 2)
    match3 = get_match(1, 2, 3, 0, 8)
    matches.append(match1)
    matches.append(match2)
    matches.append(match3)
    variable.calculate(matches)
    assert variable.sum == 2
    assert variable.count == 1
    assert variable.get_output_value() == 2


class TestObject():
    pass


def test_build_computed_stats():
    to = TestObject()
    match1 = get_match(1, 1, 2, 3, 0)
    build_computed_stats(match1,to)
    assert to.home_points == 3
    assert to.away_points == 0

    to2 = TestObject()
    match2 = get_match(1, 1, 2, 3, 3)
    build_computed_stats(match2, to2)
    assert to2.home_points == 1
    assert to2.away_points == 1

    to3 = TestObject()
    match3 = get_match(1, 1, 2, 1, 3)
    build_computed_stats(match3, to3)
    assert to3.home_points == 0
    assert to3.away_points == 3
