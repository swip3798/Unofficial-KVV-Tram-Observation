import json
import os
import kvvapi


def create_empty_file(name):
	f = open(name, "w")
	f.write("[]")
	f.close()

def main():
	route_id = input("Enter the route id: ")
	name = input("Enter route destination: ")
	enter = ""
	filename = route_id + "_" + name + ".json"
	create_empty_file(filename)
	enter = input("Enter stop_id of the next stop:")
	while enter != "stop":
		data = []
		with open(filename, "r") as f:
			data = json.loads(f.read())
			result = kvvapi.get_stop_by_id("de:" + enter)
			if result != None:
				data.append({"stop_id":result.stop_id, "name":result.name, "lat":result.lat, "lon":result.lon})
			else:
				print("Wrong stop_id", "de: " + enter)
		with open(filename, "w") as f:
			f.write(json.dumps(data, indent = 4, sort_keys = True))
		enter = input("Enter stop_id of the next stop: ")



if __name__ == '__main__':
	while True:
		main()