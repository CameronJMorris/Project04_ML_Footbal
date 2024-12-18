from Yardage_Models.Pass_Yardage import Pass_Yardage
from Play_Type_Classifier.Overall_Classifier import *
from Yardage_Models.Incomplete import *
from Yardage_Models.Run_Yardage import *

class General_Yardage:
    # innit contains all the classifiers and models needed to determine the overall play
    def __init__(self, data, OTeam, DTeam):
        self.data = data
        self.OTeam = OTeam
        self.DTeam = DTeam
        self.Pass = Pass_Yardage(data, OTeam, DTeam)
        self.cla = Overall_Classifier(data, OTeam, DTeam)
        self.IModel = Incomplete_Classifier(data, OTeam)
        self.run = Run_Yardage(data, OTeam, DTeam)

    # this just determines which model to call based on which classifier and inputs that data and the data inputted into the function
    def predict(self, yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential):
        play = self.cla.get_overall_play(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential)
        if play[0] == PASS:
            if self.IModel.predict(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, play[1]) == INCOMPLETE:
                return PASS, 0
            else:
                pr = self.Pass.predict(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, play[1])
                return PASS,pr

        if play[0] == RUN:
            return RUN, self.run.predict(yards_to_go, down, yards_to_TD, half_seconds_remaining, game_seconds_remaining, quarter_seconds_remaining, score_differential, play[1])