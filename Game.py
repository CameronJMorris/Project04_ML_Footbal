import random

from pygments.token import Other

import Stuff
from CONFIGS import PUNT, PLAY, FIELD_GOAL
from Yardage_Models.General_Yardage import General_Yardage
from Other.Fourth_Down import Fourth_Down

class Game:
    # this is the innit that creates everything needed and has vay too much in it
    def __init__(self, data, Team1, Team2):
        self.Team1 = Team1
        self.Team2 = Team2
        t = [Team1, Team2]
        random.shuffle(t)
        self.OTeam = t[0]
        self.DTeam = t[1]
        self.time_left_in_quarter = 900
        self.time_left_in_half = 1800
        self.time_left_in_game = 3600
        self.side_of_the_field = "" + self.OTeam
        self.Team1_score = 0
        self.Team2_score = 0
        self.Gen1 = General_Yardage(data, Team1, Team2)
        self.Gen2 = General_Yardage(data, Team2, Team1)
        self.models = {Team1:self.Gen1, Team2:self.Gen2}
        self.yard_line = 25
        self.down = 1
        self.togo = 10
        self.Fourth = Fourth_Down(data, self.OTeam)

    #pass = 0, run = 1, other = 2
    # This method changes the time of the game based on what kind of play it is, this will be changed into a model later on
    def change_time(self, num):
        time_change = 0
        if num == 0:
            time_change = 15
        if num == 1:
            time_change = 30
        if num == 2:
            time_change = 5
        if self.time_left_in_quarter >= time_change:
            self.time_left_in_quarter -= time_change
            self.time_left_in_half -= time_change
            self.time_left_in_game -= time_change
        else:
            self.time_left_in_quarter = 900
            self.time_left_in_half = ((int(self.time_left_in_half//900))*900)%1800
            self.time_left_in_game = (int(self.time_left_in_game//900))*900
        if self.time_left_in_game < 0:
            self.time_left_in_game = 0
        if self.time_left_in_half < 0:
            self.time_left_in_half = 0
        if self.time_left_in_quarter < 0:
            self.time_left_in_quarter = 0

    # this changes who has the ball and moves the ball a certain amount of yards
    def turn_over(self, net_change):
        self.move(2,net_change)
        team = self.OTeam
        self.OTeam = self.DTeam
        self.DTeam = team
        self.down = 1
        self.togo = 10

    # this moves the ball a certain amount of yards and changes the time with the previous method
    def move(self, kind, yards):
        self.togo -= yards
        if yards > self.yard_line:
            yards = self.yard_line
        if self.OTeam == self.side_of_the_field:
            if yards < (50-self.yard_line):
                self.yard_line += yards
            else:
                yards -= (50-self.yard_line)
                self.yard_line = 50 - yards
                self.side_of_the_field = self.DTeam
        else:
            if yards == self.yard_line:
                self.touchdown()
            else:
                if yards < -(50-self.yard_line):
                    self.side_of_the_field = self.OTeam
                    yards += (50 - self.yard_line)
                    self.yard_line = 50 + yards
                else:
                    self.yard_line -= yards
        self.down += 1
        if self.togo <= 0:
            self.down = 1
            self.togo = 10
        self.change_time(kind)

    # this scores a touchdown and adds
    def touchdown(self):
        print(self.OTeam + " TOUCHDOWN")
        if self.OTeam == self.Team1:
            self.Team1_score += 7
        else:
            self.Team2_score += 7
        self.turn_over(-25)

    # this simulates a field goal, this will be turned into a method for efficiency
    def field_goal(self):
        print(self.OTeam + " FIELD GOAL")
        if self.OTeam == self.Team1:
            self.Team1_score += 3
        else:
            self.Team2_score += 3
        self.yard_line = 25
        self.down = 1
        self.togo = 10
        self.turn_over(0)
        self.side_of_the_field = self.OTeam

    # this method gets the distance to end_zone to allow for easy use in predict methods
    def yards_to_TD(self):
        if self.OTeam == self.side_of_the_field:
            return 100 - self.yard_line
        else: return self.yard_line

    # this method gets the score differential to allow for easy use in predict methods
    def get_score_difference(self):
        if self.OTeam == self.Team1:
            return self.Team1_score - self.Team2_score
        return self.Team2_score - self.Team1_score

    # This method resets the game to allow for easy multi simulation
    def reset(self):
        self.yard_line = 25
        self.down = 1
        self.togo = 10
        t = [self.Team1, self.Team2]
        random.shuffle(t)
        self.OTeam = t[0]
        self.DTeam = t[1]
        self.time_left_in_quarter = 900
        self.time_left_in_half = 1800
        self.time_left_in_game = 3600
        self.side_of_the_field = "" + self.OTeam
        self.Team1_score = 0
        self.Team2_score = 0


if __name__ == "__main__":
    G = Game(Stuff.get_data(),"KC", "LV")
    while True:
        if G.down == 4:
            pred = G.Fourth.predict(G.togo, G.yards_to_TD(), G.time_left_in_half, G.time_left_in_game, G.time_left_in_quarter, G.get_score_difference())
            if pred == PLAY:
                pass
            elif pred == PUNT:
                G.turn_over(min(60, max(G.yard_line-10,G.yards_to_TD())))
            elif pred == FIELD_GOAL:
                if G.yards_to_TD() < 45:
                    G.field_goal()
                else:
                    G.turn_over(0)
        if G.down == 5:
            G.turn_over(0)
            print("Turnover on Downs")
        play, pred = G.models.get(G.OTeam).predict(G.togo, G.down, G.yards_to_TD(), G.time_left_in_half, G.time_left_in_game, G.time_left_in_quarter, G.get_score_difference())
        print(str(G.OTeam) + " "+ str(play) + " for " + str(pred) + " yards")
        G.move(1, play)

        if G.time_left_in_game == 0:
            print("time")
            quit()