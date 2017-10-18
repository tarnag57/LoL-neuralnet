"""
Loads training data and test data
Format: 
1 neuron -> score (0->1)
136 neuron -> selected champ (0/1)

Score function: f(x) = (x-1000)/2000 e.g.: 1000->0 and 3000->1, linear
"""

import numpy as np

champ_num = 136

input = open("data2", "r")
lines = input.read().splitlines()
length = len(lines)

def read_game(begin):
	"""Reads a game which begins with the line having index begin
	Returns [[input], [expected output]]
	input has (134+1)*10 = 1350 element, output has 1 element"""
	game = []
	for i in xrange(10):
		#reading champ num
		champ = int(lines[begin + i*2])
		for j in xrange(champ - 1):
			game.append(0)
		game.append(1)
		for j in xrange(champ_num - champ):
			game.append(0)	
		#reading score
		score = int(lines[begin + i*2 + 1])
		game.append((float(score) - 1000)/2000)

	result = [int(lines[begin + 20])]
	print("Length of game[]: {0}".format(len(game)))
	game_matrix = np.matrix(game)
	result_matrix = np.matrix(result)	
	data = [game_matrix, result_matrix]
	return data

def load_data(test_num):
	test_data = []
	training_data = []
	for i in xrange(0, test_num*21, 21):
		test_data.append(read_game(i))
	for i in xrange(test_num*21, length, 21):
		training_data.append(read_game(i))
	return training_data, test_data
