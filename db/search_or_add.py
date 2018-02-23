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
		result = kvvapi.get_stop_by_id(input("Enter the id you want to add: "))
		if result != None:
			obj = {"stop_id":result.stop_id, "name":result.name, "lat":result.lat, "lon":result.lon}
			data += obj
			with open("stations_db.json", "w") as f:
				f.write(json.dumps(data, indent = 4, sort_keys = True))

if __name__ == '__main__':
	while True:
		main()