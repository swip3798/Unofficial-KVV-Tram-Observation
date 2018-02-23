from os import listdir
from os.path import isfile, join
import re
import json

def listFiles():
	mypath = "."
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	only_db = []
	for i in files:
		regexp = re.compile(r'[0-9].*\.json')
		if regexp.search(i):
			only_db.append(i)
	return only_db


if __name__ == '__main__':
	data = []
	print(listFiles())
	for i in listFiles():
		data += json.loads(open(i, "r").read())
	with open("stations_db.json", "w") as f:
		f.write(json.dumps(data, indent = 4, sort_keys=True))