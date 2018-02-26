import json
import os
import kvvapi


def main():
	data = json.loads(open("stations_db.json", "r").read())
	result = kvvapi.get_stop_by_id(input("Enter the id you want to add: "))
	if result != None:
		obj = [{"stop_id":result.stop_id, "name":result.name, "lat":result.lat, "lon":result.lon}]
		print(json.dumps(obj, indent = 4, sort_keys = True))
		data = data + obj
		with open("stations_db.json", "w") as f:
			f.write(json.dumps(data, indent = 4, sort_keys = True))
	else:
		print("Is None")

if __name__ == '__main__':
	while True:
		main()