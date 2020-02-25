from enum import Enum
from FootBotApi.calculator.CalculationMethod import CalculationMethod


class ComputedFromMatchesField:
    def __init__(self, team_id, home_input_variable_name, away_input_variable_name, output_variable_name,
                 calculation_method, include_matches):
        self.team_id = team_id
        self.home_input_variable_name = home_input_variable_name
        self.away_input_variable_name = away_input_variable_name
        self.output_variable_name = output_variable_name
        self.calculation_method = calculation_method
        self.include = include_matches
        self.sum = 0
        self.count = 0
        self.average = 0

    def set_team_id(self, team_id):
        self.team_id = team_id

    def is_home(self, home_team_id):
        return home_team_id == self.team_id

    def is_away(self, away_team_id):
        return away_team_id == self.team_id

    def calculate(self, flat_matches):
        for match in flat_matches:
            if self.include == Include.ALL:
                if self.is_home(match.localteam_id):
                    self.sum += self.get_attribute(match, self.home_input_variable_name)
                elif self.is_away(match.visitorteam_id):
                    self.sum += self.get_attribute(match, self.away_input_variable_name)
                self.count += 1
            elif (self.include == Include.HOME) & self.is_home(match.localteam_id):
                self.sum += self.get_attribute(match, self.home_input_variable_name)
                self.count += 1
            elif (self.include == Include.AWAY) & self.is_away(match.visitorteam_id):
                self.sum += self.get_attribute(match, self.away_input_variable_name)
                self.count += 1

    def get_output_value(self):
        if self.calculation_method == CalculationMethod.SUM:
            return self.sum
        elif self.calculation_method == CalculationMethod.AVG:
            if self.count == 0:
                return 0
            return self.sum / float(self.count)
        elif self.calculation_method == CalculationMethod.COUNT:
            return self.count

    def set_object_attr_to_output_value(self, object_to_set):
        setattr(object_to_set, self.output_variable_name, self.get_output_value())

    @staticmethod
    def get_attribute(object_to_set, name):
        if not hasattr(object_to_set, name):
            return 0
        else:
            if getattr(object_to_set, name) is None:
                return 0
            return getattr(object_to_set, name)


class Include(Enum):
    ALL = 1
    HOME = 2
    AWAY = 3
