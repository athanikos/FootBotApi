import json


class JsonSerializable(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


# iterates through flat_,matches and computes the average of variable_to_use
# creates an object Output and sets variable_to_produce to variable_to_use/count
def compute_average(flat_matches, team_id, variable_to_use, variable_to_produce, object_to_set):
    average = 0
    count = 0
    for ft in flat_matches:
        if not hasattr(ft, variable_to_use):
            raise NameError(variable_to_use + " does not exist ")
        if ft.localteam_id == team_id:
            average += getattr(ft, variable_to_use)
            count = count + 1
        elif ft.visitorteam_id == team_id:
            average += getattr(ft, variable_to_use)
            count = count + 1
    if count == 0:
        setattr(object_to_set, variable_to_produce, 0)
        return object_to_set

    setattr(object_to_set, variable_to_produce, average / float(count))
    return object_to_set

