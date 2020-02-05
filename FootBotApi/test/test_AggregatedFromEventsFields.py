from FootBotApi.calculator.AggregatedFromEventsFields import AggregatedFromEventsFields
from FootBotApi.test.helpers import get_event


def test_AggregatedFromEventsFields():
  event1 = get_event(1, "goal", 14)
  event2 = get_event(1, "yellowcard", 14)
  events = []
  events.append(event1)
  events.append(event2)
  minutes = []
  minutes.append(15)
  minutes.append(30)
  aeff = AggregatedFromEventsFields(events,1,2,minutes)
  aeff.init_output_dictionaries()
  aeff.compute_output_values("goal",22,1)
  aeff.compute_output_values("yellowcard",2,1)
  assert aeff.home_team_goals[15] == 0
  assert aeff.home_team_goals[30] == 1
  assert aeff.home_team_yellow_cards[15] == 1
  assert aeff.home_team_yellow_cards[30] == 1


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
