from enum import Enum


class CalculatedVariable:
    def __init__(self, team_id, home_team_id, away_team_id, input_variable_name, output_variable_name,
                 calculation_method, include_matches):
        self.team_id = team_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.input_variable_name = input_variable_name
        self.output_variable_name = output_variable_name
        self.calculation_method = calculation_method
        self.include = include_matches
        self.sum = 0
        self.count = 0
        self.average = 0

    def is_home(self):
        return self.home_team_id == self.team_id

    def is_away(self):
        return self.away_team_id == self.team_id

    def calculate(self, flat_matches):
        for match in flat_matches:
            if self.include == Include.ALL:
                self.sum += getattr(match, self.input_variable_name)
                self.count += 1
            elif self.include == Include.HOME & self.is_home():
                self.sum += getattr(match, self.input_variable_name)
                self.count += 1
            elif self.include == Include.AWAY & self.is_away():
                self.sum += getattr(match, self.input_variable_name)
                self.count += 1

    def get_output_value(self):
        if self.calculation_method == Calculation_Method.SUM:
            return self.sum
        elif self.calculation_method == Calculation_Method.AVG:
            return self.sum / float(self.count)
        elif self.calculation_method == Calculation_Method.COUNT:
            return self.count

    def set_object_attr_to_output_value(self, object_to_set):
        setattr(object_to_set, self.output_variable_name, self.get_output_value())


class Calculation_Method(Enum):
    SUM = 1
    COUNT = 2
    AVG = 3


class Include(Enum):
    ALL = 1
    HOME = 2
    AWAY = 3
