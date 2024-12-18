from numpy.random import random

import Stuff
from CONFIGS import TEAMS, PASS, RUN
from Play_Type_Classifier.Offense_Classifier import Offense_Classifier
from Play_Type_Classifier.Defense_Classifier import Defense_Classifier
from Play_Type_Classifier.Specific_Classifier import Specific_Classifier
import pandas as pd

import warnings

warnings.filterwarnings('ignore')


class Overall_Classifier:
    # the innit contains all the individual classifiers to make an overall decision and then returns that
    def __init__(self, data, Oteam, Dteam):
        self.Oteam = Oteam
        self.Dteam = Dteam
        self.data = data
        if Dteam not in TEAMS or Oteam not in TEAMS:
            quit()

        self.OModel = Offense_Classifier(data, Oteam)
        self.DModel = Defense_Classifier(data, Dteam)
        self.SClass = Specific_Classifier(data, Oteam)

    # gets the prediction based on teh offensive team and defensive team, and combines them together
    def get_play(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential):
        Opred = self.OModel.predict(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining,quarter_seconds_remaining, score_differential)
        Dpred = self.DModel.predict(yards_to_TD, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential)
        Pass_prob = max(0, 1-(Opred[1] + Dpred[1]))
        #Run_prob = min(1, 1-(Opred[1] + Pass_prob))
        i = random()
        if i < Pass_prob:
            return PASS
        else: return RUN

    # this combines the previous play prediction with the more specific prediction like the gap of the air yards
    def get_overall_play(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential):
        play = self.get_play(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential)
        spec = self.SClass.predict(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, play)
        return play, spec