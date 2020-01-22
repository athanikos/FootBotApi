def compute_average_goals(flat_matches, team_id):
    average_goals = 0
    count = 0
    for ft in flat_matches:
        if ft.localteam_id == team_id:
            average_goals += ft.stats_data_0_goals
            count = count + 1
        elif ft.visitorteam_id == team_id:
            average_goals += ft.stats_data_1_goals
            count = count + 1
    if count == 0:
        return 0
    return average_goals / float(count)


def compute_average(flat_matches, team_id, variable_to_use):
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
        return 0
    return average / float(count)
