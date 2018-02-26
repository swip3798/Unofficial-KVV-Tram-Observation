import json


route_id = input("Enter the route id: ")
name = input("Enter route destination: ")
new_dest = input("New destination:")
filename = route_id + "_" + name + ".json"
filename_new = route_id + "_" + new_dest + ".json"
data = []

with open(filename, "r") as f:
	data = json.loads(f.read())

data.reverse()
with open(filename_new, "w") as f:
	f.write(json.dumps(data, indent = 4, sort_keys = True))