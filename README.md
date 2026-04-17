# ME Football Power Ranking System
## Main Idea

This is an attempt to create a ranking system for college football specifically (NFL is in here for testing and fun) using only the knowledge of the games themselves. The ranking takes all teams at a starting value of 100.0 points and will increase that score for a win and decrease it with a loss. The points added or lost depends on how good the other team is and by the difference in the game score (including overtime). The better the score of the opposing team, the more points you can gain from a win and less points will be lost from losing. However, the worse a team is, the less points can be gained and losing will take a lot more points from the overall score.

## How it Works

A loop will be run several times until the power score of every team has stabilized. The first loop is run with every team given a score of 100.0 points (note: FBS teams can play FCS teams but we do not track the score of FCS teams). The process of each loop will be:
* For each game, determine the winner, loser, how big of a difference the game score is, if the game went to overtime, and if each team is valid (NFL is always valid but FCS teams in college are invalid)
* A bonus is found determined by the difference in score with the smallest being -2 (overtime game) and the highest being +3 for NFL (difference of over 24 points) and +4 for college (difference of over 31 points)
* If both teams are valid, the determination of the gains and losses are:
  - Winner gains: minimum_value( loser score / 10.0, min_add ) + bonus
  - min_add is set to 4.0 for college and 6.0 for NFL
  - Loser loses: ( 100.0 / maximum_value( winner score / 10.0, max_loss ) ) + bonus
  - max_loss is set to 5.0 for both college and NFL
* If one of the teams are invalid, then the determination is:
  - If the valid team won, they gain: min_add - 2 note: -2 is for the lowest possible bonus
  - If the valid team lost, they lose: ( 100.0 / max_loss ) + 4 note: +4 is for the highest possible bonus
* Once every game has been run through, the score from the beginning of the loop and end of the loop are compared
* If the difference between every teams beginning and end score is less than .001, than the stable score has been found, else the loop is rerun with the beginning loop score updated

Once the stable score has been found, those will be the final power score and rankings for each team can be official.

## How to Run it

**Main.py** has the functions setup to return the final scores and will just need to run `python main.py`.
