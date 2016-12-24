# NFL-ELO

NFL-ELO is a project to attempt to give ELO rankings to each NFL team, based on their past performances.  The program then uses these ELO rankings to attempt to predict future NFL games.  The goal is to be able to reach a high percentage of accuracy in predicting the outcome of NFL games.

## Running the Program

First, install all required modules using
```bash
$ pip install -r requirements.txt
```

To run the program, generate the ELO rankings to be stored in pickle dump files.  Run

```bash
$ python gen.py
```

Once this finishes, it will print out the ELO ratings, as well as dump the necessary information to a pickle dump file.  Now run

```bash
$ python predict.py
```

This file will output the predictions made using the ELO system.

There is also a web frontend to the project to make it more easily accessible - run `python2 nfl.py` to run the web frontend on port 5001.

## Data

The data used is from the [nflgame](https://github.com/BurntSushi/nflgame) repository, dating back to 2009.

## ELO System

The ELO System used is identical to that found on [Wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system), with each team initialized at some initial ELO value, adjustable within the code.  Through each game, an expected winning percentage is calculated, and whether or not a team wins affects how the elo is adjusted.  Over the course of hundreds of games, the ELO will tend towards the theoretical "rank" of each team - better teams will bubble to the top, and worse teams will sink to the bottom.  The system is normalized such that if Team A has a certain amount of ELO, denoted as ELO_DIFF, more than Team B, then Team A will have a probability that is a certain number of times, denoted by ELO_BASE, greater than Team B to win.  These parameters can be varied and can produce different results - vary them and see which works best!

The system also takes into account the winning and losing streaks of teams - teams on a large winning streak that win again will gain more ELO, while teams who have lost many games in a row will lose more and more.  Both increase logistically, asymptotically approaching a maximum multiplier as to ensure that teams on large winning streaks do not overwhelm the rest of the teams in the standings.

The ELO of each team is "pushed" towards the initial ELO at the end of every season, as to ensure that teams who dominate the season before are not too far ahead of others in a new season, to account for roster, coaching, or system changes.  The ELO-shifting factor is also set as the difference between the winning team's score and the losing team's score, so that larger margins of victory will result in larger gains in ELO, and vice versa.  Teams in a bye week have their ELO unchanged.

Here is a screenshot of the ELO rankings generated, as of Week 10 of the 2016 NFL Season.

![Week 10, 2016](/screenshots/Screenshot_1.png?raw=true)

## Prediction

The prediction system simply uses the expected winning percentage given by the ELO rating.  The predictions are then ordered by the "most confident" to "least confident", using the difference in percentage between the team projected to win and the team projected to lose.  They are also presented in color(!) to make it more visually appealing.

Here is a screenshot of the predictions made for Week 11 using data through Week 10 of the 2016 NFL Season.

![Week 10, 2016](/screenshots/Screenshot_2.png?raw=true)

## Further Work

I intend to further develop this by making graphics, perhaps interactive, displaying the variations in ELO over the course of multiple seasons.  I also hope to vary the parameters, to find the optimal ones for predicting the outcome of games.  This may eventually lead into a Machine Learning/Neural Network project, using past games as training data and testing it on future game predictions.
