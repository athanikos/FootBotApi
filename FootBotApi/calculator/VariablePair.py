from enum import Enum


class VariablePair:
    def __init__(self, team_id, home_team_id, away_team_id, input_variable_name, output_variable_name,
                 calculation_method):
        self.team_id = team_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.input_variable_name = input_variable_name
        self.output_variable_name = output_variable_name
        self.calculation_method = calculation_method

    def is_home(self):
        return self.home_team_id == self.team_id

    def is_away(self):
        return self.away_team_id == self.team_id

    def calculate(self):
        if self.calculation_method == Calculation_Method.SUM:
            return 0
        elif self.calculation_method == Calculation_Method.COUNT:
            return 0
        elif self.calculation_method == Calculation_Method.AVG:
            return 0


class Calculation_Method(Enum):
    SUM = 1
    COUNT = 2
    AVG = 3


class Include(Enum):
    ALL = 1
    HOME = 2
    AWAY = 3