import Stuff
from CONFIGS import PLAY, PUNT, FIELD_GOAL
from Game import Game

# runs a game and returns 0 for a team 1 win, a 1 for team 2 win and .5 if the game is a tie
def run_a_game(G):
    while True:
        if G.down == 4:
            pred = G.Fourth.predict(G.togo, G.yards_to_TD(), G.time_left_in_half, G.time_left_in_game,
                                    G.time_left_in_quarter, G.get_score_difference())
            if pred == PLAY:
                pass
            elif pred == PUNT:
                G.turn_over(min(60, max(G.yard_line - 10, G.yards_to_TD())))
            elif pred == FIELD_GOAL:
                if G.yards_to_TD() < 45:
                    G.field_goal()
                else:
                    G.turn_over(0)
        if G.down == 5:
            G.turn_over(0)
            print("Turnover on Downs")
        play, pred = G.models.get(G.OTeam).predict(G.togo, G.down, G.yards_to_TD(), G.time_left_in_half,
                                                   G.time_left_in_game, G.time_left_in_quarter,
                                                   G.get_score_difference())
        print(str(G.OTeam) + " " + str(play) + " for " + str(pred) + " yards")
        G.move(1, play)

        if G.time_left_in_game == 0:
            print("time")
            if G.Team1_score > G.Team2_score:
                return 1
            elif G.Team1_score < G.Team2_score:
                return 1
            else:
                return .5

G = Game(Stuff.get_data(), "CAR", "BAL")

j = 0
for i in range(1000):
    j += run_a_game(G)
    G.reset()
    if i % 100 == 0:
        print("asdfasjdhvbjbvhasbvjabvcjakhasdjbv" + str(i/100))
print(j)