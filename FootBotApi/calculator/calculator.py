import json
from FootBotApi.calculator.AggregatedFromMatchesField import  AggregatedFromMatchesField, Include
from FootBotApi.calculator import CalculationMethod


class OutputTeamStats(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def build_stats(flat_matches, team_id, league_id, before_date,object_to_set):
    compute_aggregated_fields(flat_matches, team_id, object_to_set)
    setattr(object_to_set, "team_id", team_id)
    setattr(object_to_set, "league_id", league_id)
    setattr(object_to_set, "before_date", before_date)


def compute_fields_from_events(events, home_team_id, away_team_id):
    for event in events:
        print(event)


def compute_aggregated_fields(items_to_use, team_id, object_to_set):
    fields = [AggregatedFromMatchesField(1, 'stats_data_0_goals', 'stats_data_1_goals', 'AverageAttack', CalculationMethod.CalculationMethod.AVG,
                                         Include.HOME),
              AggregatedFromMatchesField(1, 'stats_data_1_goals', 'stats_data_0_goals', 'AverageDefence', CalculationMethod.CalculationMethod.AVG,
                                         Include.HOME),
              ]
    for field in fields:
        field.set_team_id(team_id)
        field.calculate(items_to_use)
        field.set_object_attr_to_output_value(object_to_set)
