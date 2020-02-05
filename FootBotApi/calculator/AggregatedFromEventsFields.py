RED_CARD = "redcard"
YELLOW_CARD = "yellowcard"
GOAL = "goal"
HOME_TEAM_YELLOW_CARDS = "hometeamyellowcards"
AWAY_TEAM_YELLOW_CARDS = "awayteamyellowcards"
HOME_TEAM_GOALS = "hometeamgoals"
AWAY_TEAM_GOALS = "awayteamgoals"
HOME_TEAM_RED_CARDS = "hometeamredcards"
AWAY_TEAM_RED_CARDS = "awayteamredcards"


class AggregatedFromEventsFields:

    def __init__(self, events, home_team_id, away_team_id, minutes):
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.minutes = minutes
        self.events = events
        self.home_team_yellow_cards={}
        self.away_team_yellow_cards={}
        self.home_team_red_cards={}
        self.away_team_red_cards={}
        self.home_team_goals={}
        self.away_team_goals={}

    def init_output_dictionaries(self):
        for minute in self.minutes:
            self.home_team_yellow_cards[minute] = 0
            self.away_team_yellow_cards[minute] = 0
            self.home_team_red_cards[minute] = 0
            self.away_team_red_cards[minute] = 0
            self.home_team_goals[minute] = 0
            self.away_team_goals[minute] = 0

    def is_home(self, team_id):
        return team_id == self.home_team_id

    def is_away(self, team_id):
        return team_id == self.away_team_id

    def compute_output_values(self, event_type, event_minute, team_id):
        for minute in self.minutes:
            if minute >= event_minute:
                if event_type == YELLOW_CARD:
                    if self.is_home(team_id):
                        self.home_team_yellow_cards[minute] += 1
                    elif self.is_away(team_id):
                        self.away_team_yellow_cards[minute] += 1
                elif event_type == RED_CARD:
                    if self.is_home(team_id):
                        self.home_team_red_cards[minute] += 1
                    elif self.is_away(team_id):
                        self.away_team_red_cards[minute] += 1
                elif event_type == GOAL:
                    if self.is_home(team_id):
                        self.home_team_goals[minute] += 1
                    elif self.is_away(team_id):
                        self.away_team_goals[minute] += 1

    def add_output_values_to_object(self, object_to_set):
        for key in self.home_team_yellow_cards:
            setattr(object_to_set, HOME_TEAM_YELLOW_CARDS + "_" + key, self.home_team_yellow_cards[key])
        for key in self.away_team_yellow_cards:
            setattr(object_to_set, AWAY_TEAM_YELLOW_CARDS + "_" + key, self.away_team_yellow_cards[key])
        for key in self.home_team_red_cards:
            setattr(object_to_set, HOME_TEAM_RED_CARDS + "_" + key, self.home_team_red_cards[key])
        for key in self.away_team_red_cards:
            setattr(object_to_set, AWAY_TEAM_RED_CARDS + "_" + key, self.away_team_yellow_cards[key])
        for key in self.home_team_goals:
            setattr(object_to_set, HOME_TEAM_GOALS + "_" + key, self.home_team_goals[key])
        for key in self.away_team_goals:
            setattr(object_to_set, AWAY_TEAM_GOALS + "_" + key, self.away_team_goals[key])