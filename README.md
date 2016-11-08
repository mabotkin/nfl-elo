# NFL-ELO

NFL-ELO is a project to attempt to give ELO rankings to each NFL team, based on their past performances.  The program then uses these ELO rankings to attempt to predict future NFL games.  The goal is to be able to reach a high percentage of accuracy in predicting the outcome of NFL games.

## Running the Program

To run the program, first, we must generate the ELO rankings, stored in pickle dump files.  Run

```bash
$ python gen.py
```

Once this finishes, it will print out the ELO ratings, as well as dump the necessary information to a pickle dump file.  Now run

```bash
$ python predict.py
```

This file will output the predictions made using the ELO system.

## Data

The data used is from the [nflgame](https://github.com/BurntSushi/nflgame) repository, dating back to 2009.

## ELO System

The ELO System used is identical to that found on [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system), with each team initialized at 1200 ELO.  Through each game, an expected winning percentage is calculated, and whether or not a team wins affects how the elo is adjusted.  Over the course of hundreds of games, the ELO will tend towards the theoretical "rank" of each team - better teams will bubble to the top, and worse teams will sink to the bottom.  The system is normalized such that if Team A has 400 more ELO than Team B, then Team A will have 10 times the probability of beating Team B.  These parameters can be varied and can produce different results - vary them and see which works best!

The ELO of each team is "pushed" towards the initial ELO at the end of every season, as to ensure that teams who dominate the season before are not too far ahead of others in a new season, to account for roster, coaching, or system changes.  The ELO-shifting factor is also set as the difference between the winning team's score and the losing team's score, so that larger margins of victory will result in larger gains in ELO, and vice versa.  Teams in a bye week have their ELO unchanged.

Here is a screenshot of the ELO rankings generated, as of Week 9 of the 2016 NFL Season.

![Week 9, 2016](/screenshots/screenshot2.png?raw=true)

## Prediction

The prediction system simply uses the expected winning percentage given by the ELO rating.  The predictions are then ordered by the "most confident" to "least confident", using the difference in percentage between the team projected to win and the team projected to lose.  They are also presented in color(!) to make it more visually appealing.

Here is a screenshot of the predictions made for Week 10 using data through Week 9 of the 2016 NFL Season.

![Week 9, 2016](/screenshots/screenshot1.png?raw=true)

## Further Work

I intend to further develop this by making graphics, perhaps interactive, displaying the variations in ELO over the course of multiple seasons.  I also hope to vary the parameters, to find the optimal ones for predicting the outcome of games.  This may eventually lead into a Machine Learning/Neural Network project, using past games as training data and testing it on future game predictions.
