file = open("champ_list", "r")
champs = file.read().splitlines()
file.close()

in_put = open("data.txt", "r")
lines = in_put.read().splitlines()
in_put.close()

output = open("data2", "a")

for line in lines:
	try:
		int_line = int(line)
		output.write(line + "\n")
	except:
		if line == "Bardo":
			line = "Bard"

		cur = 0
		for champ in champs:
			if champ == line:
				output.write(str(cur) + "\n")	
				continue
			else:
				cur = cur + 1
		if cur == 136:
			print("Error converting {0}".format(line))



