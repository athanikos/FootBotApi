import json
from FootBotApi.calculator.ComputedFromMatchesField import  ComputedFromMatchesField, Include
from FootBotApi.calculator import CalculationMethod
from FootBotApi.calculator.ComputedField import ComputedField, ComputedFormula,Operator


class OutputTeamStats(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def build_historical_stats(flat_matches, team_id, league_id, before_date, object_to_set):
    compute_historical_fields(flat_matches, team_id, object_to_set)
    setattr(object_to_set, "team_id", team_id)
    setattr(object_to_set, "league_id", league_id)
    setattr(object_to_set, "before_date", before_date)


def build_computed_stats(object_to_get_values, object_to_set_values):
    home_points_formulas =  [ ComputedFormula('stats_data_0_goals', 'stats_data_1_goals',Operator.GREATER_THAN,3,1,object_to_get_values ) ,
                   ComputedFormula('stats_data_0_goals', 'stats_data_1_goals', Operator.EQUAL, 1, 0,object_to_get_values),
                   ComputedFormula('stats_data_0_goals', 'stats_data_1_goals', Operator.LESS_THAN, 0, 0, object_to_get_values),
                   ]
    hcf = ComputedField('home_points', object_to_get_values,object_to_set_values,  home_points_formulas)
    hcf.compute()

    away_points_formulas =  [ ComputedFormula('stats_data_0_goals', 'stats_data_1_goals',Operator.LESS_THAN ,3,1,object_to_get_values ) ,
                   ComputedFormula('stats_data_0_goals', 'stats_data_1_goals', Operator.EQUAL, 1, 0,object_to_get_values),
                   ComputedFormula('stats_data_0_goals', 'stats_data_1_goals', Operator.GREATER_THAN, 0, 0, object_to_get_values),
                   ]
    acf = ComputedField('away_points', object_to_get_values,object_to_set_values, away_points_formulas)
    acf.compute()


def compute_historical_fields(items_to_use, team_id, object_to_set):
    fields = [ComputedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'AverageAttack', CalculationMethod.CalculationMethod.AVG,
                                       Include.HOME),
              ComputedFromMatchesField(1, 'stats_data_1_goals', 'stats_data_0_goals', 'AverageDefence', CalculationMethod.CalculationMethod.AVG,
                                       Include.HOME),
              ]
    for field in fields:
        field.set_team_id(team_id)
        field.calculate(items_to_use)
        field.set_object_attr_to_output_value(object_to_set)
