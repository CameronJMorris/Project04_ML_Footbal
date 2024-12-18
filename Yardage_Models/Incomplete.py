from random import random

from sklearn.linear_model import LogisticRegression

from CONFIGS import TEAMS, COMPLETE, INCOMPLETE


class Incomplete_Classifier:
    # makes the model/classifier and include important fields
    def __init__(self, data, team):
        self.data = data
        self.team = team
        self.model = LogisticRegression()
        if self.team not in TEAMS:
            quit()
        self.filter_Data()
        self.fit()

    # this filters the data and makes sure that it works as it is supposed to and also makes sure the offense team is the only data columns and that they are only passes
    def filter_Data(self):
        filtered_data = self.data[self.data['offteam'].isin([str(self.team)])].copy()
        filtered_data = filtered_data[filtered_data['play_type'].isin([str("pass")])].copy()
        self.data = filtered_data

    # this fits the model with whether the pass is complete or not
    def fit(self):
        X = self.data[["ydstogo", "down", "Yards_To_TD", "half_seconds_remaining", "game_seconds_remaining", "quarter_seconds_remaining", "score_differential", "air_yards"]]
        y = self.data['incomplete_pass']
        X_clean = X.dropna()
        y_clean = y[X_clean.index]
        self.model.fit(X_clean, y_clean)

    # returns incomplete of complete based on what the model predicts and this is random and based on the probabilities given
    def predict(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, air_yards):
        pred = self.model.predict_proba([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining,quarter_seconds_remaining, score_differential, air_yards]])
        i = random()
        if i < pred[0][0]:
            return COMPLETE
        else:
            return INCOMPLETE