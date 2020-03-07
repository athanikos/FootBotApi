from FootBotApi.models import flatmatches, Event


def get_match(league_id, local_team_id, visitor_team_id, stats_data_0_goals, stats_data_1_goals):
    match = flatmatches()
    match.league_id = league_id
    match.localteam_id = local_team_id
    match.visitorteam_id = visitor_team_id
    match.stats_data_0_goals = stats_data_0_goals
    match.stats_data_1_goals = stats_data_1_goals
    return match

def get_event(team_id, event_type, minute):
    e = Event()
    e.team_id = team_id
    e.type = type
    e.minute = minute
    return e