UNDERSCORE = "_"
UPTO = "UP_TO_"
RED_CARD = "redcard"
YELLOW_CARD = "yellowcard"
GOAL = "goal"
HOME_TEAM_YELLOW_CARDS = "HOME_TEAM_YELLOW_CARDS"
AWAY_TEAM_YELLOW_CARDS = "AWAY_TEAM_YELLOW_CARDS"
HOME_TEAM_GOALS = "HOME_TEAM_GOALS"
AWAY_TEAM_GOALS = "AWAY_TEAM_GOALS"
HOME_TEAM_RED_CARDS = "HOME_TEAM_RED_CARDS"
AWAY_TEAM_RED_CARDS = "AWAY_TEAM_RED_CARDS"

minutes = [14, 29, 44, 59, 74, 89]


class AggregatedFromEventsFields:

    def __init__(self, events, match_id, home_team_id, away_team_id, _minutes):
        self.match_id = match_id
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.minutes = _minutes
        self.events = events
        self.home_team_yellow_cards = {}
        self.away_team_yellow_cards = {}
        self.home_team_red_cards = {}
        self.away_team_red_cards = {}
        self.home_team_goals = {}
        self.away_team_goals = {}

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

    def compute_output_values_from_events(self):
        for e in self.events:
            self.compute_output_values(e.type, e.minute, e.team_id)

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
        setattr(object_to_set, 'match_id', self.match_id)
        setattr(object_to_set, 'home_team_id', self.home_team_id)
        setattr(object_to_set, 'away_team_id', self.away_team_id)
        for key in self.home_team_yellow_cards:
            setattr(object_to_set, HOME_TEAM_YELLOW_CARDS + UNDERSCORE + UPTO + str(key),
                    self.home_team_yellow_cards[key])
        for key in self.away_team_yellow_cards:
            setattr(object_to_set, AWAY_TEAM_YELLOW_CARDS + UNDERSCORE + UPTO + str(key),
                    self.away_team_yellow_cards[key])
        for key in self.home_team_red_cards:
            setattr(object_to_set, HOME_TEAM_RED_CARDS + UNDERSCORE + UPTO + str(key), self.home_team_red_cards[key])
        for key in self.away_team_red_cards:
            setattr(object_to_set, AWAY_TEAM_RED_CARDS + UNDERSCORE + UPTO + str(key), self.away_team_yellow_cards[key])
        for key in self.home_team_goals:
            setattr(object_to_set, HOME_TEAM_GOALS + UNDERSCORE + UPTO + str(key), self.home_team_goals[key])
        for key in self.away_team_goals:
            setattr(object_to_set, AWAY_TEAM_GOALS + UNDERSCORE + UPTO + str(key), self.away_team_goals[key])
