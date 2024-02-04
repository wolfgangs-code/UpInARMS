#!/usr/bin/env python3

from random import random
import datetime
import time
import requests
import re
import json
import sys


def main():
	toLog("[" + str(datetime.datetime.today()) + "]\n")
	ids = genIDList()
	watch = time.time()
	# If no CLI arguments are given, run the UI
	if len(sys.argv) < 2:
		for i in ids:
			# List every agency by 'ID - Name'
			print(str(i).ljust(3) + " - " + ids[i][0])
		print("--- - ---\n0   - Download All " +
			  str(len(ids)) + " Agencies (SLOW)\n")
		while True:
			selection = input("Select an Agency ID >")
			try: selection = int(selection)
			except:
				print("The ID must be an integer.")
				continue
			if selection in ids or {0}: break
			else:
				print("Invalid agency ID.")
				continue
		if selection == 0:
			watch = time.time()
			for i in ids:
				getAllData(i, ids[i][0], ids[i][1])
		else:
			watch = False
			getAllData(selection, ids[selection][0], ids[selection][1])
	elif int(sys.argv[1]) == 0:
		for i in ids:
			getAllData(i, ids[i][0], ids[i][1])
	else:
		for n in sys.argv:
			if n != sys.argv[0]:
				try: getAllData(n, ids[int(n)][0], ids[int(n)][1])
				except KeyError:
					print("AgencyID {} does not exist!".format(n))
					toLog(" + Failed to download invalid agencyID [{}]\n".format(n))
	#=================================#
	# Post-download procedure         #
	# Everything has been successful! #
	#=================================#
	msg = " = Completed Successfully"
	if watch != False:
		msg += " (" + ("{:.2f}".format(time.time() - watch)) + ")"
	toLog(msg + "\n\n")
	exit()


def getAllData(id, name, st):
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	watch = time.time()
	# Starting page number: Keep at 1!
	p = 1
	records = {}
	print("Downloading {} [{}]".format(name,str(id)))
	while True:
		try:
			r = requests.get(buildURL(id, p))
			jsn = json.loads(r.text)
		except requests.exceptions.ConnectionError:
			toLog(" + Connection Error! Retrying...\n")
			time.sleep(1)
			continue
		except json.decoder.JSONDecodeError:
			toLog(" + JSON Decoding Error! Skipping page {} in AgencyID {}\n".format(p,id))
			p += 1
			continue
		# Prepare the JSON file's contents
		file = {"agencyID": id,
				"agencyName": name,
				"agencyCountry": "USA",  # So there's no ambiguity
				"agencyState": st,
				"records": jsn["records"],
				"scrapeDate": date,
				"data": records}
		# Dictionary trash
		for row in jsn["rows"]:
			records[row.pop("id")] = row.pop("cell")
		f = open("output/agencyID-" + str(id) + ".json", "w")
		f.write(json.dumps(file, indent=4))
		f.close
		timer = "{:.2f}".format(time.time() - watch)
		if jsn["page"] < jsn["total"]:
			p += 1
			print("- page {} of {}".format(str(p), str(jsn["total"])))
			continue
		else:
			toLog(" - Downloaded [{}] {} ({}s)\n".format(str(id), name, timer))
			break


# Constructs a valid URL to access the past 2048 records from an agency over a decade
def buildURL(id, page):
	url = "https://portal.arms.com/Home/DetailsRequest?page=" + str(page)
	crimes = ""
	for i in range(1, 28):
		crimes += "&CrimeTypesIds=" + str(i)
	x = datetime.datetime.now()
	y = x - datetime.timedelta(days=365 * 20)
	toDay = x.strftime("%m/%d/%y")
	bDay = y.strftime("%m/%d/%y")
	rows = (4096)
	fake = "{:.16f}".format(random())
	# Bob the Builder
	comp = url + "&rows={}&AgencyId={}{}".format(str(rows), str(id), crimes)
	comp += "&fakeID={}&beginDate={}&endDate={}".format(fake, bDay, toDay)
	return comp


def genIDList():
	r = requests.get("https://portal.arms.com/")
	pattern = r"agenciesItems:(.*),\s"
	rgx = re.search(pattern, r.text).group(1)
	ids = {}
	for i in json.loads(rgx):
		state = i["DisplayingName"][:2]
		ids[i["Id"]] = [i["Name"], state]
	return ids


def toLog(msg):
	log = open("log.txt", "a")
	log.write(msg)
	log.close()


main()
