
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
    return average_goals / float(count)



