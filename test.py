import random
import urllib2, cookielib

from cassiopeia import riotapi
from bs4 import BeautifulSoup #html parsing
from time import sleep

riotapi.set_region("EUNE")
riotapi.set_api_key("RGAPI-fea9f643-7979-4b87-b857-a8330157d2c8")

summoner = riotapi.get_summoner_by_name("petisa")
index = 1


def ping_summoner(summoner_name):
	site = "http://www.lolskill.net/summoner/EUNE/{name}/champions".format(name = summoner_name)
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    	   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	
	#rerfreshing statistics on LoLSikills
	req = urllib2.Request(site, headers = hdr)
	page = urllib2.urlopen(req)
	
	site = "http://b.scorecardresearch.com/beacon.js"
	hdr = {'Host': 'b.scorecardresearch.com',
		   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
		   'Accept': '*/*',
		   'Accept-Language': 'en-US,en;q=0.5',
		   'Accept-Encoding': 'gzip, deflate',
		   'Referer': "http://www.lolskill.net/summoner/EUNE/{name}/champions".format(name = summoner.name.encode('utf-8')),
		   'Connection': 'keep-alive'}
	
	req = urllib2.Request(site, headers = hdr)
	page = urllib2.urlopen(req)	
	

def champ_score(summoner_name, champ_name):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    	   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	
	site = "http://www.lolskill.net/summoner/EUNE/{name}/champions".format(name = summoner_name)
	req = urllib2.Request(site, headers = hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()

	content = page.read()
	#print content

	champ_index = content.find("with {name}".format(name = champ_name))
	score_begin = content.find("\"", champ_index) + 2
	score_end = content.find("<", score_begin)

	score = ""

	#formating
	if score_begin + 4 < score_end:
		score = score + content[score_begin : score_end - 4]
		score_begin = score_end - 3

	score = score + content[score_begin:score_end]
	score_int = int(float(score))
	return score_int


#get last match
match_list = summoner.match_list()
match_ref = match_list[index]
match = match_ref.match()

#who played who
for participant in match.participants:
	ping_summoner(participant.summoner.name.encode('utf-8'))
	
sleep(1)	

for participant in match.participants:
	print("Looking up: " + participant.summoner.name.encode('utf-8') + " with champ: " + participant.champion.name)
	score = champ_score(participant.summoner.name.encode('utf-8'), participant.champion.name)
	print("Player: {player} Selected Champion: {champ} Score: {score}".format(player = participant.summoner.name.encode('utf-8'), champ = participant.champion.name, score = score))

#did he win
if match.participants[0].stats.win:
	print("Blue won")
else:
	print("Red won")
