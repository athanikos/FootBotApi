from mongoengine import *


class flatmatches(Document):
    league_id = IntField()
    localteam_id = IntField()
    visitorteam_id = IntField()
    visitorTeam_data_name = StringField()
    localTeam_data_name = StringField()
    time_starting_at_date = StringField()
    time_status = StringField()
    time_minute = IntField()
    stats_data_1_goals = IntField()
    stats_data_0_goals = IntField()
    id = IntField()
    time_extra_minute = IntField()
    stats_data_0_corners = IntField()
    stats_data_1_shots_ongoal = IntField()
    stats_data_1_yellowredcards = IntField()
    time_starting_at_time = IntField()
    league_id = IntField()
    stats_data_0_attacks_dangerous_attacks = IntField()
    stats_data_1_corners = IntField()
    scores_localteam_score = IntField()
    time_second = IntField()
    stats_data_0_passes_total = IntField()
    stats_data_1_fixture_id = IntField()
    stats_data_1_injuries = IntField()
    stats_data_0_injuries = IntField()
    stats_data_1_passes_total = IntField()
    stats_data_1_redcards = IntField()
    stats_data_1_shots_offgoal = IntField()
    standings_localteam_position = IntField()
    time_starting_at_date_time = IntField()
    stats_data_1_yellowcards = IntField()
    stats_data_0_shots_total = IntField()
    referee_id = IntField()
    stats_data_0_shots_ongoal = IntField()
    scores_visitorteam_score = IntField()
    stats_data_0_yellowcards = IntField()
    stats_data_0_shots_blocked = IntField()
    stats_data_0_substitutions = IntField()
    stats_data_1_goal_attempts = IntField()
    attendance = IntField()
    visitorteam_id = IntField()
    assistants_fourth_official_id = IntField()
    stats_data_0_possessiontime = IntField()
    stats_data_1_passes_accurate = IntField()
    stats_data_0_passes_accurate = IntField()
    time_injury_time = IntField()
    stats_data_1_throw_in = IntField()
    stats_data_1_attacks_dangerous_attacks = IntField()
    assistants_second_assistant_id = IntField()
    stats_data_0_throw_in = IntField()
    stats_data_1_ball_safe = IntField()
    stats_data_1_team_id = IntField()
    _id = IntField()
    stats_data_1_shots_outsidebox = IntField()
    stats_data_0_offsides = IntField()
    stats_data_0_redcards = IntField()
    stats_data_0_passes_percentage = IntField()
    stats_data_0_shots_insidebox = IntField()
    coaches_visitorteam_coach_id = IntField()
    stats_data_1_passes_percentage = IntField()
    stats_data_0_team_id = IntField()
    stats_data_0_goal_attempts = IntField()
    stats_data_0_yellowredcards = IntField()
    stats_data_1_shots_total = IntField()
    coaches_localteam_coach_id = IntField()
    stats_data_1_penalties = IntField()
    stats_data_1_goal_kick = IntField()
    stats_data_1_shots_blocked = IntField()
    stats_data_0_saves = IntField()
    stats_data_0_penalties = IntField()
    stats_data_1_shots_insidebox = IntField()
    stats_data_1_substitutions = IntField()
    stats_data_0_attacks_attacks = IntField()
    standings_visitorteam_position = IntField()
    stats_data_0_shots_outsidebox = IntField()
    time_starting_at_timestamp = IntField()
    time_starting_at_timezone = IntField()
    stats_data_0_fixture_id = IntField()
    stats_data_1_fouls = IntField()
    stats_data_0_free_kick = IntField()
    stats_data_1_offsides = IntField()
    venue_id = IntField()
    stats_data_1_attacks_attacks = IntField()
    stats_data_1_free_kick = IntField()
    stats_data_0_ball_safe = IntField()
    stats_data_1_possessiontime = IntField()
    stats_data_0_shots_offgoal = IntField()
    stats_data_0_goal_kick = IntField()
    assistants_first_assistant_id = IntField()
    time_added_time = IntField()
    stats_data_1_saves = IntField()
    stats_data_0_fouls = IntField()
    stats_data_1_passes = IntField()
    stats_data_0_passes = IntField()


class Event(EmbeddedDocument):
    id = IntField()
    team_id = IntField()
    type = StringField()
    related_player_id = IntField()
    related_player_name = StringField()
    extra_minute = IntField()
    player_name = StringField()
    player_id = IntField()
    injuried = IntField()
    result = IntField()
    fixture_id = IntField()
    reason = IntField()
    minute = IntField()
    result = StringField()


class StartingAt(EmbeddedDocument):
    date_time = StringField()
    date =  StringField()
    time = StringField()
    timestamp = IntField()
    timezone = StringField()


class Time(EmbeddedDocument):
    status = StringField()
    starting_at = EmbeddedDocumentField(StartingAt, db_field='starting_at')
    second = StringField()
    added_time = StringField()
    minute = IntField()
    extra_minute = IntField()
    injury_time = IntField()


class matches(Document):
    id = IntField()
    localteam_id = IntField()
    league_id = IntField()
    visitorteam_id = IntField()
    events = ListField(EmbeddedDocumentListField(Event, db_field='data'))
    time = EmbeddedDocumentField(Time, db_field='time')
    inplay = IntField()
    scores = IntField()
    round_id = IntField()
    attendance = IntField()
    commentaries = IntField()
    differenceAt75 = IntField()
    aggregate_id = IntField()
    weather_report = IntField()
    formations = IntField()
    assistants = IntField()
    season_id = IntField()
    visitorTeam = IntField()
    group_id = IntField()
    stats = IntField()
    deleted = IntField()
    pitch = IntField()
    colors = IntField()
    _id = IntField()
    coaches = IntField()
    flatOdds = IntField()
    odds = IntField()
    winning_odds_calculated = IntField()
    winner_team_id = IntField()
    venue_id = IntField()
    leg = IntField()
    referee_id = IntField()
    stage_id = IntField()
    localTeam = IntField()
    standings = IntField()
    neutral_venue =IntField()
    details = IntField()
