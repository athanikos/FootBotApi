import json

CNT = "cnt"
SUM = "sum"
input_output_pairs = {"stats_data_0_goals": 'out', "stats_data_1_goals": 'out2'}

variables = []

class OutputTeamStats(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


def build_stats(flat_matches, team_id, league_id, before_date,object_to_set):
    compute_average(flat_matches,team_id,input_output_pairs, object_to_set)
    setattr(object_to_set, "team_id", team_id)
    setattr(object_to_set, "league_id", league_id)
    setattr(object_to_set, "before_date", before_date)


def compute_average(flat_matches, team_id, variable_pairs, object_to_set):
    for variable in variable_pairs:
        key = variable.input_variable_name
        init_value(variable_pairs, key, object_to_set, CNT)
        init_value(variable_pairs, key, object_to_set, SUM)
        for ft in flat_matches:
            if not hasattr(ft, key):
                raise NameError(key + " does not exist ")
            if ft.localteam_id == team_id:
                increment_sum_value(variable_pairs, key, object_to_set, getattr(ft, key))
                set_next_count_value(variable_pairs, key, object_to_set)
            elif ft.visitorteam_id == team_id:
                increment_sum_value(variable_pairs, key, ft, getattr(ft, key))
                set_next_count_value(variable_pairs, key, object_to_set)
    for variable in variable_pairs:
        key = variable.input_variable_name
        if get_count_value(variable_pairs, key, object_to_set) == 0:
            setattr(object_to_set, variable_pairs[key], 0)
        else:
            setattr(object_to_set, variable_pairs[key], get_sum_value(variable_pairs, key, object_to_set)
                    / float(get_count_value(variable_pairs, key, object_to_set)))
    return object_to_set


def get_count_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from, name_pairs[key] + CNT):
        setattr(object_to_get_from, name_pairs[key] + CNT, 0)
    return getattr(object_to_get_from, name_pairs[key] + CNT)


def get_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from,  key):
        setattr(object_to_get_from, key, 0)
    return getattr(object_to_get_from, key)


def get_sum_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from, name_pairs[key] + SUM):
        setattr(object_to_get_from, name_pairs[key] + SUM, 0)
    return getattr(object_to_get_from, name_pairs[key] + SUM)


def set_next_count_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from, name_pairs[key] + CNT):
        setattr(object_to_get_from, name_pairs[key] + CNT, 0)
    setattr(object_to_get_from, name_pairs[key] + CNT, get_count_value(name_pairs, key, object_to_get_from) + 1)


def init_value(name_pairs, key, object_to_get_from, postfix):
    setattr(object_to_get_from, name_pairs[key] + postfix, 0)


def increment_sum_value(name_pairs, key, object_to_get_from, value):
    if value is None:
        value = 0

    if not hasattr(object_to_get_from, name_pairs[key] + SUM):
        setattr(object_to_get_from, name_pairs[key] + SUM, value)
    else:
        setattr(object_to_get_from, name_pairs[key] + SUM,
                get_sum_value(name_pairs, key, object_to_get_from) + value)
