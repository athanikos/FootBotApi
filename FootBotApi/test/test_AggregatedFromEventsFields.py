from FootBotApi.calculator.AggregatedFromEventsFields import AggregatedFromEventsFields
from FootBotApi.test.helpers import get_event, get_match


def test_AggregatedFromEventsFields():
    event1 = get_event(1, "goal", 14)
    event2 = get_event(1, "yellowcard", 14)
    events = []
    events.append(event1)
    events.append(event2)
    minutes = []
    minutes.append(15)
    minutes.append(30)
    aeff = AggregatedFromEventsFields(events, 1, 2, minutes)
    aeff.init_output_dictionaries()
    aeff.compute_output_values("goal", 22, 1)
    aeff.compute_output_values("yellowcard", 2, 1)
    assert aeff.home_team_goals[15] == 0
    assert aeff.home_team_goals[30] == 1
    assert aeff.home_team_yellow_cards[15] == 1
    assert aeff.home_team_yellow_cards[30] == 1


def test_AggregatedFromEventsFields_Away():
    event1 = get_event(2, "goal", 14)
    event2 = get_event(2, "yellowcard", 14)
    events = []
    events.append(event1)
    events.append(event2)
    minutes = []
    minutes.append(15)
    minutes.append(30)
    aeff = AggregatedFromEventsFields(events, 1, 2, minutes)
    aeff.init_output_dictionaries()
    aeff.compute_output_values("goal", 22, 2)
    aeff.compute_output_values("yellowcard", 2, 2)
    assert aeff.away_team_goals[15] == 0
    assert aeff.away_team_goals[30] == 1
    assert aeff.away_team_yellow_cards[15] == 1
    assert aeff.away_team_yellow_cards[30] == 1


def test_AggregatedFromEventsFields_Null_Events():
    minutes = []
    minutes.append(15)
    minutes.append(30)
    aeff = AggregatedFromEventsFields(None, 1, 2, minutes)
    aeff.init_output_dictionaries()
    assert aeff.home_team_goals[15] == 0
    assert aeff.home_team_goals[30] == 0
    assert aeff.away_team_goals[15] == 0
    assert aeff.away_team_goals[30] == 0
    assert aeff.home_team_yellow_cards[15] == 0
    assert aeff.home_team_yellow_cards[30] == 0
    assert aeff.away_team_yellow_cards[15] == 0
    assert aeff.away_team_yellow_cards[30] == 0
    assert aeff.home_team_red_cards[15] == 0
    assert aeff.home_team_red_cards[30] == 0
    assert aeff.away_team_red_cards[15] == 0
    assert aeff.away_team_red_cards[30] == 0


def test_add_output_values_to_object():
    event1 = get_event(1, "goal", 14)
    event2 = get_event(1, "yellowcard", 14)
    events = []
    events.append(event1)
    events.append(event2)
    minutes = []
    minutes.append(15)
    minutes.append(30)
    aeff = AggregatedFromEventsFields(events, 1, 2, minutes)
    aeff.init_output_dictionaries()
    aeff.compute_output_values("goal", 22, 1)
    aeff.compute_output_values("yellowcard", 2, 1)
    out = TestOut()
    aeff.add_output_values_to_object(out)
    assert out.HOME_TEAM_YELLOW_CARDS_UP_TO_15 == 1
    assert out.HOME_TEAM_YELLOW_CARDS_UP_TO_30 == 1
    assert out.HOME_TEAM_RED_CARDS_UP_TO_30 == 0
    assert out.HOME_TEAM_RED_CARDS_UP_TO_15 == 0


def test_add_output_values_to_object_matches():
    match1 = get_match(1, 1, 2, 3, 0)
    event1 = get_event(1, "goal", 14)
    event2 = get_event(1, "yellowcard", 14)
    events = []
    events.append(event1)
    events.append(event2)
    minutes = []
    minutes.append(15)
    minutes.append(30)
    aeff = AggregatedFromEventsFields(events, 1, 2, minutes)
    aeff.init_output_dictionaries()
    aeff.compute_output_values("goal", 22, 1)
    aeff.compute_output_values("yellowcard", 2, 1)
    aeff.add_output_values_to_object(match1)
    assert match1.HOME_TEAM_YELLOW_CARDS_UP_TO_15 == 1
    assert match1.HOME_TEAM_YELLOW_CARDS_UP_TO_30 == 1
    assert match1.HOME_TEAM_RED_CARDS_UP_TO_30 == 0
    assert match1.HOME_TEAM_RED_CARDS_UP_TO_15 == 0

class TestOut():
    pass
