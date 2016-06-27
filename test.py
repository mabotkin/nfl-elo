import nflgame

games = nflgame.games(2014)
players = nflgame.combine_game_stats(games)
for p in players.passing().sort('passing_yds').limit(5):
	msg = '%s : %d yds'
	print msg % (p,p.passing_yds)
