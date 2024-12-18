from scipy.stats import skewnorm
from sklearn.linear_model import QuantileRegressor
from Yardage_Models.Incomplete import *
from Play_Type_Classifier import Overall_Classifier
from Play_Type_Classifier.Overall_Classifier import Overall_Classifier

class Run_Yardage:
    # the innit that contains everything and initializes the model.
    def __init__(self, data, OTeam, DTeam):
        self.data = data
        self.OTeam = OTeam
        self.DTeam = DTeam
        self.model_low = QuantileRegressor(quantile=.2, alpha=.01)  # 10th percentile yardage
        self.model_mid = QuantileRegressor(quantile=.5, alpha=.01)  # 50th percentile yardage
        self.model_high = QuantileRegressor(quantile=.8, alpha=.01)  # 90th percentile yardage
        self.filter_data()
        self.fit()

    # this filters the data and makes sure that it works as it is supposed to and also adds a new column("gap") that has a number for which gap the run is through
    def filter_data(self):
        filtered_data = self.data[self.data['offteam'].isin([str(self.OTeam)])].copy()
        filtered_data = filtered_data[filtered_data['play_type'].isin([str("run")])].copy()
        filtered_data = filtered_data[filtered_data['run_gap'].isin([str("guard"), str("tackle"), str("end")])].copy()
        filtered_data["gap"] = filtered_data["run_gap"].apply(lambda x: 0 if x == "guard" else 1 if x == "tackle" else 2)
        self.data = filtered_data

    # this fits the model with each of the tree different models and drops any of the rows that are empty
    def fit(self):
        X = self.data[["ydstogo", "down", "Yards_To_TD", "half_seconds_remaining", "game_seconds_remaining",
                        "quarter_seconds_remaining", "score_differential", "gap"]]
        y = self.data['yards_gained']
        X_clean = X.dropna()
        y_clean = y[X_clean.index]
        self.model_low.fit(X_clean, y_clean)
        self.model_mid.fit(X_clean, y_clean)
        self.model_high.fit(X_clean, y_clean)

    # this predicts the yardage gained using a random level based on a skewed graph and three Quantile Regressor models and makes a random prediction based on it in a way that has higher probability for events that happen more often
    def predict(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, position):
        yards_10 = self.model_low.predict(([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, position]]))
        yards_50 = self.model_mid.predict(([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, position]]))
        yards_90 = self.model_high.predict(([[yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, position]]))
        StandardDeviation = (yards_90[0] - yards_10[0]) / 1.68
        skew = (yards_90[0] - yards_50[0]) / (yards_50[0] - yards_10[0])
        y_pred = skewnorm.rvs(a=skew, loc=yards_50, scale=StandardDeviation)
        return int(y_pred + .5)