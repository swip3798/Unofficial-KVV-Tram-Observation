import json
import os
import kvvapi


def main():
	data = json.loads(open("stations_db.json", "r").read())

	term = input("Term: ")
	results = []

	for i in data:
		if i["name"].lower().find(term.lower()) != -1:
			results.append(i)

	if results != []:
		for i in results:
			print(json.dumps(i, indent = 4, sort_keys = True))
	else:
		print("Nothing found...")

if __name__ == '__main__':
	while True:
		main()