import random
import urllib2, cookielib

from cassiopeia import riotapi
import json

#database file
data = open("data.txt", "a")


riotapi.set_region("EUNE")
riotapi.set_api_key("RGAPI-fea9f643-7979-4b87-b857-a8330157d2c8")

summoner = riotapi.get_summoner_by_name("petisa")
index = 1

#get last match
match_list = summoner.match_list()
match_ref = match_list[index]
match = match_ref.match()

matches = []

def champ_score(summoner_id):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    	   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	
	site = "http://www.lolking.net/summoner/eune/{s_id}".format(s_id = summoner_id)
	
	req = urllib2.Request(site, headers = hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()

	content = page.read()
	
	tag_begin = content.find("\"summoner-stat\"")
	tag_begin = tag_begin + 41
	tag_end = content.find("</strong", tag_begin)
	score = content[tag_begin:tag_end]
	score_int = int(float(score))
	return score_int

class Player:
	
	def __init__(self, champ, score):
		self.champ = champ
		self.score = score

class Match:
	
	def __init__(self):
		self.players = []
		self.won = ''
		
	def addPlayer(self, player):
		self.players.append(player)
		
	def whoWon(self, won):
		self.won = won

new_match = Match()		
for participant in match.participants:
	#print("Looking up: " + participant.summoner.name.encode('utf-8'))
	score = champ_score(participant.summoner.id)
	player = Player(participant.champion.name, score)
	new_match.addPlayer(player)
	data.write("{champ}\n{score}\n".format(champ = participant.champion.name, score = score))	
	print("Player: {player} Selected Champion: {champ} Score: {score}".format(player = participant.summoner.name.encode('utf-8'), champ = participant.champion.name, score = score))

#did he win
if match.participants[0].stats.win:
	print("Blue won")
	data.write("0\n")
	new_match.whoWon('blue')
else:
	print("Red won")
	data.write("1\n")
	new_match.whoWon('red')

