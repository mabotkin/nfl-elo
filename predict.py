import nflgame
from termcolor import colored
from pickle import load
from lxml import html
import requests

#schedule URL
URL = "http://www.espn.com/nfl/schedule/_/week/10"
YEAR = 2016
WEEK = 10

team_to_index = load( open( "teamindex.pkl", "rb"))
elos = load( open( "elo.pkl", "rb"))
config = load( open( "config.pkl", "rb"))

ELO_DIFF = config["ELO_DIFF"]
ELO_BASE = config["ELO_BASE"]
START_YEAR = config["START_YEAR"]

page = requests.get(URL)
tree = html.fromstring(page.content)

games1 = tree.xpath('//tr[@class="odd"]/td/a[@class="team-name"]/abbr/text()')
games2 = tree.xpath('//tr[@class="even"]/td/a[@class="team-name"]/abbr/text()')

games = []

#weave them
while not(len(games1) == 0 and len(games2) == 0):
	if len(games1) > 0:
		games.append((games1[0], games1[1]))
		games1.pop(0)
		games1.pop(0)
	if len(games2) > 0:
		games.append((games2[0], games2[1]))
		games2.pop(0)
		games2.pop(0)

print str(YEAR) + " Season: Week " + str(WEEK) + " Predictions:"
print "-------------------------------------"
print colored("0%-10%", "cyan"), colored("10%-20%", "green"), colored("20%-30%", "yellow"), colored("30%-40%","magenta"), colored("40%+", "red")
print "-------------------------------------"
for game in games:
	hname = nflgame.standard_team(game[1])
	aname = nflgame.standard_team(game[0])
	if(hname == "LA"):
		hname = "STL"
	if(aname == "LA"):
		aname = "STL"
	hteam = team_to_index[hname]
	ateam = team_to_index[aname]
	eloA = elos[hteam][WEEK][YEAR-START_YEAR]
	eloB = elos[ateam][WEEK][YEAR-START_YEAR]
	Ea = 1/(1 + ELO_BASE**((eloB - eloA)/ELO_DIFF))
	Eb = 1/(1 + ELO_BASE**((eloA - eloB)/ELO_DIFF))
	diff = abs(Ea - Eb)
	if diff < 0.1:
		col = "cyan"
	elif diff < 0.2:
		col = "green"
	elif diff < 0.3:
		col = "yellow"
	elif diff < 0.4:
		col = "magenta"
	else:
		col = "red"
	if Ea > Eb:
		hcname = colored(hname, col)
		acname = aname
	elif Eb > Ea:
		hcname = hname
		acname = colored(aname, col)
	else:
		pass
	print acname + " @ " + hcname + ": " + aname + " - " + str(100*Eb) + "% | " + hname + " - " + str(100*Ea) + "%"
