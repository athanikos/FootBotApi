import json

from FootBotApi.calculator.CalculatedField import CalculatedField, Calculation_Method, Include

CNT = "cnt"
SUM = "sum"


variables = []
first = CalculatedField(1, 'stats_data_0_goals', 'out', Calculation_Method.AVG, Include.HOME)
second = CalculatedField(1, 'stats_data_1_goals', 'out2', Calculation_Method.AVG, Include.HOME)
variables.append(first)
variables.append(second)


class OutputTeamStats(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def build_stats(flat_matches, team_id, league_id, before_date,object_to_set):
    compute_average(flat_matches, team_id, object_to_set)
    setattr(object_to_set, "team_id", team_id)
    setattr(object_to_set, "league_id", league_id)
    setattr(object_to_set, "before_date", before_date)


def compute_average(flat_matches, team_id, object_to_set):
    for field in variables:
        field.calculate(flat_matches)
        field.set_object_attr_to_output_value(object_to_set)
