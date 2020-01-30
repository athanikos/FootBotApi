from enum import Enum


class CalculatedField:
    def __init__(self, team_id, input_variable_name, output_variable_name,
                 calculation_method, include_matches):
        self.team_id = team_id
        self.input_variable_name = input_variable_name
        self.output_variable_name = output_variable_name
        self.calculation_method = calculation_method
        self.include = include_matches
        self.sum = 0
        self.count = 0
        self.average = 0

    def is_home(self, home_team_id):
        return home_team_id == self.team_id

    def is_away(self,away_team_id):
        return away_team_id == self.team_id

    def calculate(self, flat_matches):
        for match in flat_matches:
            if self.include == Include.ALL:
                self.sum += getattr(match, self.input_variable_name)
                self.count += 1
            elif (self.include == Include.HOME) & self.is_home(match.localteam_id):
                self.sum += getattr(match, self.input_variable_name)
                self.count += 1
            elif (self.include == Include.AWAY) & self.is_away(match.visitorteam_id):
                self.sum += getattr(match, self.input_variable_name)
                self.count += 1

    def get_output_value(self):
        if self.calculation_method == Calculation_Method.SUM:
            return self.sum
        elif self.calculation_method == Calculation_Method.AVG:
            if self.count == 0:
                return 0
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
