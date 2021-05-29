from random import random
import datetime
import requests
import re
import json


def main():
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
    getAllData(selection)
    exit()


def getAllData(id):
	p = 1
	r = requests.get(buildURL(id, p))
	jsn = json.loads(r.text)
	f = open("agencyID" + str(id) + "-" + str(p) + ".json", "w")
	f.write(json.dumps(jsn))
	f.close



# Constructs a valid URL to access the past 2048 records from an agency over a decade
def buildURL(id, page):
	url = "https://portal.arms.com/Home/DetailsRequest?page=" + str(page)
	crimes = ""
	for i in range(1,28):
		crimes += "&CrimeTypesIds=" + str(i)
	x = datetime.datetime.now()
	y = x - datetime.timedelta(days=3650)
	toDay  = x.strftime("%m/%d/%y")
	bDay =   y.strftime("%m/%d/%y")
	rows =   2048
	fake =   "{:.16f}".format(random())
	# Bob the Builder
	comp  = url + "&rows=" + str(rows) + "&AgencyId=" + str(id) + crimes
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
