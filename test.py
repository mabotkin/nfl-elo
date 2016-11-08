import nflgame

START_YEAR = 2009
CUR_YEAR = 2016
CUR_WEEK = 9
REG_WEEKS = 17
POST_WEEKS = 4
INIT_ELO = 1200

def eloEval(eloA, eloB, scoreA, scoreB):
	diff = abs(eloA - eloB)
	if scoreA == scoreB:
		if eloA < eloB:
			eloA += (0.2)*diff
			eloB -= (0.2)*diff
		elif eloB < eloA:
			eloA -= (0.2)*diff
			eloB += (0.2)*diff
	elif scoreA > scoreB:
		if eloA < eloB:
			eloA += (0.3)*diff
			eloB -= (0.3)*diff
		elif eloB < eloA:
			eloA -= (0.1)*diff
			eloB += (0.1)*diff
		else:
			diff = scoreA - scoreB
			eloA += (0.2)*diff
			eloB -= (0.2)*diff
	elif scoreA < scoreB:
		if eloA < eloB:
			eloA -= (0.1)*diff
			eloB += (0.1)*diff
		elif eloB < eloA:
			eloA += (0.3)*diff
			eloB -= (0.3)*diff
		else:
			diff = scoreB - scoreA
			eloA -= (0.2)*diff
			eloB += (0.2)*diff
	return int(eloA), int(eloB)
		

WEEKS_PER_YEAR = REG_WEEKS + POST_WEEKS

# elos[teamid][week][year]
elos = [[[0 for i in range(CUR_YEAR-START_YEAR+1)] for i in range(WEEKS_PER_YEAR+1)] for i in range(len(nflgame.teams)-1)]

team_to_index = {}

ind = 0
for i in nflgame.teams:
	if i[0] == "LA":
		continue
	team_to_index[i[0]] = ind
	elos[ind][0][0] = INIT_ELO
	ind += 1

for i in range(START_YEAR, CUR_YEAR + 1):
	print "Processing " + str(i) + " season"
	for j in range(1,WEEKS_PER_YEAR+1):
		try:
			if not (i == CUR_YEAR and j > CUR_WEEK):
				if(j <= REG_WEEKS):
					games = nflgame.games(i,week=j,kind='REG')
					#print "Processing Week " + str(j) + " of " + str(i) + " season"
				else:
					games = nflgame.games(i,week=j-REG_WEEKS,kind='POST')
					#print "Processing Postseason Week " + str(j-REG_WEEKS) + " of " + str(i) + " season"
				if len(games) > 0:
					for game in games:
						hname = nflgame.standard_team(game.home)
						aname = nflgame.standard_team(game.away)
						if(hname == "LA"):
							hname = "STL"
						if(aname == "LA"):
							aname = "STL"
						hteam = team_to_index[hname]
						ateam = team_to_index[aname]
						elos[hteam][j][i-START_YEAR], elos[ateam][j][i-START_YEAR] = eloEval(elos[hteam][j-1][i-START_YEAR], elos[ateam][j-1][i-START_YEAR], game.score_home, game.score_away)
		except TypeError:
			if(j <= REG_WEEKS):
				print "Error in Week " + str(j) + " of " + str(i) + " season"
			else:
				print "Error in Postseason Week " + str(j-REG_WEEKS) + " of " + str(i) + " season"
		for x in range(len(nflgame.teams)-1): # check for byes
			if elos[x][j][i-START_YEAR] == 0:
				elos[x][j][i-START_YEAR] = elos[x][j-1][i-START_YEAR] 
		#end of year, smoosh everyone towards middle
	if i != CUR_YEAR:
		for x in range(len(nflgame.teams)-1):
			elos[x][0][i-START_YEAR+1] = (elos[x][WEEKS_PER_YEAR][i-START_YEAR] + INIT_ELO)/2

# print final elos
rank = []
for i in nflgame.teams:
	if i[0] == "LA":
		continue
	rank.append((elos[team_to_index[i[0]]][WEEKS_PER_YEAR][CUR_YEAR-START_YEAR],i[0]))

rank = sorted(rank, reverse=True)
print "Final ELO Rankings:"
for i in range(len(rank)):
	print str(i+1) + ": " + rank[i][1] + " - ELO: " + str(rank[i][0])
