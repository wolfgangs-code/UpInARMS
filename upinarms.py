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
    print("amogus")


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
