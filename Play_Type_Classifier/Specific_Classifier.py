import math

import numpy as np
from numpy.random import random
from scipy.stats import skewnorm
from sklearn.linear_model import LogisticRegression, QuantileRegressor
from sklearn.preprocessing import StandardScaler

from CONFIGS import TEAMS, RUN, PASS, GUARD, TACKLE, END


class Specific_Classifier:
    # this is the innit that contains all the models, and the two different datas, the scalar, for the passing, and then calls fit and filter for both
    def __init__(self, data, Oteam):
        self.dataR = data.copy()
        self.dataP = data.copy()
        self.Oteam = Oteam
        self.modelR = LogisticRegression()
        self.modelP_10 = QuantileRegressor(quantile=.2, alpha=.01)  # 10th percentile yardage
        self.modelP_50 = QuantileRegressor(quantile=.5, alpha=.01)  # 50th percentile yardage
        self.modelP_90 = QuantileRegressor(quantile=.8, alpha=.01)  # 90th percentile yardage
        self.scalar = StandardScaler()
        if self.Oteam not in TEAMS:
            quit()
        self.filter_DataR()
        self.filter_DataP()
        self.fitR()
        self.fitP()

    # filters the rushing data and gets the gap position sorted in the way of 0, 1, and 2s based on where it isand gets the right team and makes sure that it is a run
    def filter_DataR(self):
        filtered_data = self.dataR[self.dataR['offteam'].isin([str(self.Oteam)])].copy()
        filtered_data = filtered_data[filtered_data['play_type'].isin([str("run")])].copy()
        filtered_data = filtered_data[filtered_data['run_gap'].isin([str("guard"), str("tackle"), str("end")])].copy()
        filtered_data["gap_position"] = filtered_data["run_gap"].apply(lambda x: 0 if x == "guard" else 1 if x == "tackle" else 2)
        self.dataR = filtered_data

    # filters the pass data and gets the air yards sorted in case it does not exist and gets the right team and makes sure that it is a pass
    def filter_DataP(self):
        filtered_data = self.dataP[self.dataP['offteam'].isin([str(self.Oteam)])].copy()
        filtered_data = filtered_data[filtered_data['play_type'].isin([str("pass")])].copy()
        filtered_data["air_yards"] = filtered_data["air_yards"].apply(lambda x: 0 if math.isnan(x) else x)
        self.dataP = filtered_data

    # fits the model to which gap position it is and make sures there are no problems with the data
    def fitR(self):
        X = self.dataR[["ydstogo", "down", "Yards_To_TD", "half_seconds_remaining", "game_seconds_remaining",
                       "quarter_seconds_remaining", "score_differential"]]
        y = self.dataR['gap_position']
        X_clean = X.dropna()
        y_clean = y[X_clean.index]
        self.modelR.fit(X_clean, y_clean)

    # fits the data to the passing models and it will predict the air yars, and it makes sure that the air yards exist since it can be finicky
    def fitP(self):
        X = self.dataP[["ydstogo", "down", "Yards_To_TD", "half_seconds_remaining", "game_seconds_remaining",
                       "quarter_seconds_remaining", "score_differential"]]
        y = self.dataP['air_yards']
        X_clean = X.dropna()
        y_clean = y[X_clean.index]
        X_clean = self.scalar.fit_transform(X_clean)
        self.modelP_10.fit(X_clean, y_clean)
        self.modelP_50.fit(X_clean, y_clean)
        self.modelP_90.fit(X_clean, y_clean)

    # decides which model to use based on which kind of play it is and then returns what it is accordingly
    def predict(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, kind):
        if kind == RUN:
            pred = self.modelR.predict_proba([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential]])
            guard = pred[0][0]
            tackle = pred[0][1]
            end = pred[0][2]
            i = random()
            if i < guard:
                return GUARD
            if i < tackle:
                return TACKLE
            else:
                return END
        if kind == PASS:
            yards_10 = self.modelP_10.predict(self.scalar.transform([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential]]))
            yards_50 = self.modelP_50.predict(self.scalar.transform([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential]]))
            yards_90 = self.modelP_90.predict(self.scalar.transform([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential]]))
            StandardDeviation = (yards_90[0] - yards_10[0]) / 1.68
            skew = (yards_90[0] - yards_50[0]) / (yards_50[0] - yards_10[0])
            y_pred = skewnorm.rvs(a=skew, loc=yards_50, scale=StandardDeviation)
            return int(y_pred +.5)