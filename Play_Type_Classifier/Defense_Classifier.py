from sklearn.linear_model import LogisticRegression

from CONFIGS import TEAMS


class Defense_Classifier:
    # makes an innit with the defensive team and makes the model and then class filter data and fit
    def __init__(self, data, team):
        self.data = data
        self.team = team
        self.model = LogisticRegression()
        if self.team not in TEAMS:
            quit()
        self.filter_Data()
        self.fit()
    # this filters the data and makes sure that it works as it is supposed to and also changes a column("Play_Called") that makes the values 0 if pass and 1 for a run and makes sure it is the right defensive team and only contains runs and passes
    def filter_Data(self):
        filtered_data = self.data[self.data['defteam'].isin([str(self.team)])].copy()
        filtered_data = filtered_data[filtered_data['play_type'].isin([str("run"), str("pass")])].copy()
        filtered_data["Play_Called"] = filtered_data["play_type"].apply(lambda x: 1 if x == "run" else 0)
        self.data = filtered_data

    # this fits the model with whether the play was a run or not
    def fit(self):
        X = self.data[["ydstogo", "down", "Yards_To_TD", "half_seconds_remaining", "game_seconds_remaining", "quarter_seconds_remaining", "score_differential"]]
        y = self.data['Play_Called']
        X_clean = X.dropna()
        y_clean = y[X_clean.index]
        self.model.fit(X_clean, y_clean)

    # uses the model of the class to make a prediction and then return this prediction(the prediction is probability of two different plays)
    def predict(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential):
        pred = self.model.predict_proba([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining,quarter_seconds_remaining, score_differential]])
        return (pred[0][0], pred[0][1])