from FootBotApi.calculator.AggregatedFromMatchesField import AggregatedFromMatchesField
from FootBotApi.calculator.calculator import OutputTeamStats, compute_aggregated_fields, build_stats
from FootBotApi.test.helpers import get_match
from FootBotApi.calculator.AggregatedFromMatchesField import  Include
from FootBotApi.calculator.CalculationMethod import  CalculationMethod


def test_build_stats():
    matches = []
    match1 = get_match(1, 1, 2, 1, 0)
    matches.append(match1)
    object_to_set = OutputTeamStats()
    variable_pairs =[]
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG,
                                          Include.ALL)
    variable_pairs.append(variable)
    build_stats(matches, 1, 1, "1/1/2010", object_to_set)
    assert getattr(object_to_set, "team_id") == 1
    assert getattr(object_to_set, "league_id") == 1
    assert getattr(object_to_set, "before_date") == "1/1/2010"


def test_CalculatedVariable_calculate():
     variable =  AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG,
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


def test_CalculatedVariable_calculate_SUM():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.SUM, Include.HOME)
    matches = []
    match1 = get_match(1, 1, 2, 3, 0)
    match2 = get_match(1, 1, 2, 2, 0)
    matches.append(match1)
    matches.append(match2)
    variable.calculate(matches)
    assert variable.sum == 5
    assert variable.count == 2
    assert variable.get_output_value() == 5


def test_CalculatedVariable_calculate_SUM_ALL():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.SUM, Include.ALL)
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


def test_CalculatedVariable_calculate_COUNT_ALL():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.COUNT, Include.HOME)
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


def test_CalculatedVariable_calculate_AWAY_AVG():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG, Include.AWAY)
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

def test_CalculatedVariable_calculate_AWAY_COUNT():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.COUNT, Include.AWAY)
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


def test_CalculatedVariable_calculate_AWAY_AVG_ZERO():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.AVG, Include.AWAY)
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

def test_CalculatedVariable_calculate_AWAY_SUM():
    variable = AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'out', CalculationMethod.SUM, Include.AWAY)
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