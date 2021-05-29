from random import random
import datetime
import requests
import re
import json
import sys


def main():
	if len(sys.argv) < 2:
		ids = genIDList()
		for i in ids:
			print(str(i).ljust(3) + " - " + ids[i])
			print("--- - ---\n0   - Download All " + str(len(ids)) + " Agencies\n")
		while True:
			selection = input("Select an Agency ID >")
			try:
				selection = int(selection)
			except:
				print("The ID must be an integer.")
				continue
			if selection in ids or {0}:
				break
			else:
				print("Invalid agency ID.")
				continue
	else:
		selection = sys.argv[1]
	getAllData(selection)
	# exit()


def getAllData(id):
	date = datetime.datetime.now().strftime("%Y-%m-%d")
	p = 1
	records = {}
	while True:
		r = requests.get(buildURL(id, p))
		jsn = json.loads(r.text)
		file = {"agencyID": id,
				"records": jsn["records"],
				"scrapeDate": date,
				"data": records}
		for row in jsn["rows"]:
			records[row.pop("id")] = row.pop("cell")
		f = open("agencyID-" + str(id) + ".json", "w")
		f.write(json.dumps(file, indent=4))
		f.close
		if jsn["page"] < jsn["total"]:
			print("Downloading page " + str(p) + " of " + str(jsn["total"]))
			p += 1
			continue
		else:
			print("Download complete.")
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
	rows = 2 ** 12
	fake = "{:.16f}".format(random())
	# Bob the Builder
	comp = url + "&rows=" + str(rows) + "&AgencyId=" + str(id) + crimes
	comp += "&fakeID=" + fake + "&beginDate=" + bDay + "&endDate=" + toDay
	return comp


def getAgencyData():
	r = requests.get("https://portal.arms.com/")
	pattern = r"agenciesItems:(.*),\s"
	rgx = re.search(pattern, r.text).group(1)
	return json.loads(rgx)


def genIDList():
	agents = getAgencyData()
	ids = {}
	for i in agents:
		ids[i["Id"]] = i["Name"]
	return ids


main()
