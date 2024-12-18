import pandas as pd

# gets the distance to a touchdown from the row of the df
def yards_to_TD(row):
    Oteam = row["offteam"]
    s = row["yrdln"]
    Dteam = row["defteam"]
    if s is None or Oteam is None or Dteam is None:
        return None
    a = s.split(" ")
    if Dteam == a[0]:
        return a[1]
    else:
        return 100 - int(a[1])

# gets the offensive tea from a row of the df
def get_off_team(row):
    def_team = row["defteam"]
    away = row["away_team"]
    home = row["home_team"]
    if str(def_team) == str(away):
        return home
    return away

# gets the total points from a row of the df
def total_points(row):
    home = row["total_home_score"]
    away = row["total_away_score"]
    return int(home) + int(away)

# makes the df from the filename that was downloaded and the adds the new axes
def get_data():
    flie_Name = "/Users/26morris/Desktop/MLAI/Project04/play_by_play_2023.parquet"
    df = pd.read_parquet(flie_Name, engine='auto')
    df["offteam"] = df.apply(get_off_team, axis=1)
    df["Yards_To_TD"] = df.apply(yards_to_TD, axis=1)
    df["Total_Points"] = df.apply(total_points, axis=1)
    return df


