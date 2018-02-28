import kvvapi
import requests
import json
import interactive_map


def find_trams(route_id, destination1, destination2):
	destination = destination1
	destination_file = destination2
	filename = "db/" + str(route_id) + "_" + destination_file + ".json"
	route = json.loads(open(filename, "r").read())
	stations = []
	print("Loading route_data...")
	for n, i in enumerate(route):
		all_departures = kvvapi.get_departures(i["stop_id"])
		departures = []
		for i in all_departures:
			if i.route == str(route_id) and (i.destination == destination or destination_file == i.destination):
				departures.append(i)
			else:
				pass
				#print(i.route, i.destination, i.stopPosition)
		if departures != []:
			stations.append(departures)
		else:
			route.pop(n)
	interactive_map.createInteractiveMap(route, "map.html", "CartoDB Positron")

	print("Analyse postitions of trams...")
	results = []
	for n, i in enumerate(stations):
		if n<=len(stations)-2:
			if i[0].time > stations[n+1][0].time:
				results.append([route[n], route[n+1]])
	return [route, results, stations]







if __name__ == '__main__':
	answer = find_trams("3", "Tivoli über Hbf", "Tivoli")
	map = interactive_map.Map(answer[0], "CartoDB Positron", [49.00994599, 8.39640733])
	map.render_marker(answer[2])
	positions = []
	for i in answer[0]:
		positions.append([i["lat"],i["lon"]])
	map.render_paths(positions, color="#03f")
	'''
	positions = []
	for i in results:
		positions.append([i[0]["lat"],i["lon"]])
	'''
	map.save("map_int.html")