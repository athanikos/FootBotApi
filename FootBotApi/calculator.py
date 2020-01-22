import json

CNT = "cnt"
AVG = "avg"


class JsonSerializable(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def compute_average(flat_matches, team_id, name_pairs, object_to_set):
    for key in name_pairs:
        init_average_value(name_pairs, key, object_to_set)
        init_count_value(name_pairs, key, object_to_set)
        for ft in flat_matches:
            if not hasattr(ft, key):
                raise NameError(key + " does not exist ")
            if ft.localteam_id == team_id:
                increment_average_value (name_pairs, key, object_to_set, getattr(ft, key))
                set_next_count_value(name_pairs, key, object_to_set)
            elif ft.visitorteam_id == team_id:
                increment_average_value (name_pairs, key, ft, getattr(ft, key))
                set_next_count_value(name_pairs, key, object_to_set)
    for key in name_pairs:
        if get_count_value(name_pairs, key,object_to_set) == 0:
            setattr(object_to_set, name_pairs[key], 0)
        else:
            setattr(object_to_set, name_pairs[key], get_average_value(name_pairs, key, object_to_set)
                    / float(get_count_value(name_pairs, key, object_to_set)))
    return object_to_set


def get_count_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from, name_pairs[key] + CNT):
        setattr(object_to_get_from, name_pairs[key] + CNT, 0)
    return getattr(object_to_get_from, name_pairs[key] + CNT)


def get_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from,  key):
        setattr(object_to_get_from, key, 0)
    return getattr(object_to_get_from, key)


def get_average_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from,  name_pairs[key] + AVG):
        setattr(object_to_get_from, name_pairs[key] + AVG, 0)
    return getattr(object_to_get_from, name_pairs[key] + AVG)


def set_next_count_value(name_pairs, key, object_to_get_from):
    if not hasattr(object_to_get_from, name_pairs[key] + CNT):
        setattr(object_to_get_from, name_pairs[key] + CNT, 0)
    setattr(object_to_get_from, name_pairs[key] + CNT, get_count_value(name_pairs, key, object_to_get_from) + 1)


def init_count_value(name_pairs, key, object_to_get_from):
    setattr(object_to_get_from, name_pairs[key] + CNT, 0)


def init_average_value(name_pairs, key, object_to_get_from):
    setattr(object_to_get_from, name_pairs[key] + AVG, 0)


def increment_average_value(name_pairs, key, object_to_get_from, value):
    if not hasattr(object_to_get_from, name_pairs[key] + AVG):
        setattr(object_to_get_from, name_pairs[key] + AVG, value)
    else:
        setattr(object_to_get_from, name_pairs[key] + AVG, get_average_value(name_pairs, key, object_to_get_from) +  value)
