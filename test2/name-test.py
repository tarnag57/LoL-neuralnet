# coding=utf-8

"""Test for a champ-list
"""

from cassiopeia import riotapi

#riotparams
riotapi.set_region("EUW")
riotapi.set_api_key("RGAPI-fea9f643-7979-4b87-b857-a8330157d2c8")

file = open("champ_list", "r")

champs = file.read().splitlines()

for champ in champs:
	xxx = riotapi.get_champion_by_name(champ)
	try:
		status = riotapi.get_champion_by_name(champ)
	except:
		print("Error while looking up {0}".format(champ))



