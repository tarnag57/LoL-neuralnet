# coding=utf-8

import random
import urllib2, cookielib

from cassiopeia import riotapi

#riotparams
riotapi.set_region("BR")
riotapi.set_api_key("RGAPI-fea9f643-7979-4b87-b857-a8330157d2c8")

#super params "Facen", "iG Carrzy",
players = ["Céos", "kadaki", "Super Minerva", "Cat Noír", "duende do calaba", "danmf", "TSM PENGPONG", "Hydrogen", "EFAP", "Juzinho", "1 Jugger", "Josedeodo", "RedBért", "Rafael BelomO2", "Little Rookie11", "KsImorTal", "Mid Carente", "cnT Mills", "pimpimenta", "Ver você de novo", "Aegon Targaryien", "Cabuloso1"]
num = 100
saved = 0

#iterations
it = 0

def champ_score(summoner_id):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    	   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}
	
	site = "http://www.lolking.net/summoner/br/{s_id}".format(s_id = summoner_id)
	
	req = urllib2.Request(site, headers = hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
		return -1

	content = page.read()
	
	tag_begin = content.find("\"summoner-stat\"")
	tag_begin = tag_begin + 41
	tag_end = content.find("</strong", tag_begin)
	score = content[tag_begin:tag_end]
	score_int = -1
	try:
		score_int = int(float(score))
	except:
		print("An error occured while converting score for {player}. Score: {score}".format(player = summoner_id, score = score))
	return score_int

def game_stats(match):

	good = 0
	points = []
	champs = []

	#collect every person
	for participant in match.participants:
		#print("Looking up: " + participant.summoner.name.encode('utf-8'))
		score = champ_score(participant.summoner.id)
		if score == -1:
			break
		good = good + 1
		points.append(score)
		champs.append(participant.champion.name)
	
	
	if good == 10:

		#open data file
		data = open("data.txt", "a")		

		for i in range(0,10):
			try:
				data.write("{champ}\n{score}\n".format(champ = champs[i].encode('utf-8'), score = points[i]))
			except:
				print("Failed writing out: {champ} and {score}".format(champ = champs[i].encode('utf-8'), score = points[i]))				
			print("Writing out: {champ} and {score}".format(champ = champs[i], score = points[i]))
	
		#determine who won
		if match.participants[0].stats.win:
			data.write("0\n")
		else:
			data.write("1\n")

		#close file
		data.close()

def scan_player(name, num, it):
	#go through every match played
	tries = 0
	while tries < 5:
		try:
			summoner = riotapi.get_summoner_by_name(name)
			tries = 50
		except:
			tries = tries + 1
			print("Failed loking up {name}, tried {tries} times".format(name = name, tries = tries))
	
	#if failed looking up
	if tries == 5: return		
	
	try:
		match_list = summoner.match_list()
	except:
		print("Failed accessing summoner: {0}".format(name))
		return


	for index in range(0,num):

		#trying 3 times
		tries = 0
		while tries < 3:
			try:
				if it >= saved:
					print("Currently looking up the {index}th game of {summoner}".format(index = index, summoner = name))
					match_ref = match_list[index]
					match = match_ref.match()
					game_stats(match)
					it = it + 1
					print("Saved {it} games".format(it = it))

				else:
					it = it + 1

				#skipping loop
				tries = 5

			except:
				print("An error occured, tried {num} times".format(num = tries))
				tries = tries + 1
				

#go through every player
for player in players:
	scan_player(player, num, it)
