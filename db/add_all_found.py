import json
import os
import kvvapi


def main():
	data = json.loads(open("stations_db.json", "r").read())
	result = kvvapi.search_stop(input("Enter the term you want to add: "))
	obj = []
	if result != None:
		for i in result:
			obj.append({"stop_id":i.stop_id, "name":i.name, "lat":i.lat, "lon":i.lon})
		print(json.dumps(obj, indent = 4, sort_keys = True))
		data = data + obj
		with open("stations_db.json", "w") as f:
			f.write(json.dumps(data, indent = 4, sort_keys = True))
	else:
		print("Is None")

if __name__ == '__main__':
	while True:
		main()