from random import random

from sklearn.linear_model import LogisticRegression

from CONFIGS import TEAMS, COMPLETE, INCOMPLETE, PLAY, FIELD_GOAL, PUNT


class Fourth_Down:
    # has the innit with the classifier model and calls filter data and fit
    def __init__(self, data, team):
        self.data = data
        self.team = team
        self.model = LogisticRegression()
        if self.team not in TEAMS:
            quit()
        self.filter_Data()
        self.fit()

    # this filters the data and makes sure that it works as it is supposed to and also makes sure the offense team is the only data columns and that they are only passes, runs, punts, or field goals, and that it is 4th down and makes a column("decision"), which is which decision they made(Play:0, Punt: 1, Field Goal:2)
    def filter_Data(self):
        filtered_data = self.data[self.data['offteam'].isin([str(self.team)])].copy()
        filtered_data = filtered_data[filtered_data['down'].isin([(4)])].copy()
        filtered_data = filtered_data[filtered_data['play_type'].isin([str("pass"), str("run"), str("punt"), str("field_goal")])].copy()
        filtered_data["decision"] = filtered_data["play_type"].apply(lambda x: 0 if x == "pass" else 0 if x == "run" else 1 if x =="punt" else 2 if x == "field_goal" else 3)
        self.data = filtered_data

    # fits the model to the decision and drops any wierd or empty lines
    def fit(self):
        X = self.data[["ydstogo", "Yards_To_TD", "half_seconds_remaining", "game_seconds_remaining", "quarter_seconds_remaining", "score_differential"]]
        y = self.data['decision']
        X_clean = X.dropna()
        y_clean = y[X_clean.index]
        self.model.fit(X_clean, y_clean)

    # Predicts what the play would be using random chance using the probability method of the classifier
    def predict(self, yards_to_go, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential):
        pred = self.model.predict_proba([[yards_to_go, yards_to_TD, half_seconds_remaining, game_seconds_remaining,quarter_seconds_remaining, score_differential]])
        i = random()
        if i < pred[0][0]:
            return PLAY
        elif i < pred[0][1]:
            return PUNT
        else:
            return FIELD_GOAL