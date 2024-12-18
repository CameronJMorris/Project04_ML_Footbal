# Football Prediction AI Project
## Credits
- Chatgpt - I used chatgpt for debugging by giving it error messages and asking a few other questions related to syntax
## How to run the program
- To start the program can either go into the Game.py file and change the teams there, or you can go into the simulation file and change the teams there if you would like to simulate multiple games and then at teh end, it will print a recap as a number of how many games teh second team won
## What I would do next
- My next actions with this project would be to try different models and also include more models to include more complexity and deal with turnovers more.
## How it works
### Play_Type_Classifier
- This directory contains four different files, that together spit out a small bit about the chosen play using both the offense and defense, as well as many other facts about the current state of the game. It will say whether it was a run or a pass and the which gap, they ran through or the air yards on the pass.
### Yardage_Model
- This directory contains four different modules that together predict the yardage on the play based on what it is. Two of the both the passing and running ones are quantile regressors, and contain different percentile points, and then there is a yard gain that is predicted at semi-random, with weights being based upon this skewwed funtion with varrying numbers of highs and lows. This allows it to have a good deal of variablity with how the games goes.
