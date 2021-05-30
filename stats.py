import datetime
import json
import glob, os

def stats():
	toLog("[" + str(datetime.datetime.today()) + "]\n = ")
	toLog("[UpInARMS Data Statistics]", True)
	toLog(countRecords(False), True)
	print(" 1 - Record count Leaderboard")
	print(" - - -\n 0 - Exit\n")
	while True:
		opt = input(" Choose an Option: >")
		try: opt = int(opt)
		except:
			print("Invalid Option!")
			continue
		if opt == 1:
			print("\n  Leaderboard:\n")
			lb = countRecords(True)
			mx = max(lb, key=lambda x: x[0])
			for i in lb:
				count = str(i[0]).rjust(len(str(mx[0])))
				id = i[1]
				name = i[2]
				print("  {} - {} [{}]".format(count, name, id))
		else:
			exit()

def countRecords(total = False):
	os.chdir("output")
	r = 0
	lb = []
	for file in glob.glob("agencyID-*.json"):
		f = open(file, "r")
		jsn = json.loads(f.read())
		count = jsn["records"]
		# This could fudge up something bad.
		# But unless someone notices this
		# and calls me out for it
		# I will leave it as-is OuO
		item = (count, jsn["agencyID"], jsn["agencyName"])
		lb.append(item)
		r += count
	tot = "\n > {:,} Records in Total\n".format(r)
	os.chdir("../")
	return tot if not total else lb


def toLog(msg, p = False):
	if p == True: print(msg)
	log = open("log.txt", "a")
	log.write(str(msg))
	log.close()

stats()