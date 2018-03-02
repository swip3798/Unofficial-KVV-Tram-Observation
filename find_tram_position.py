import kvvapi
import requests
import json
import time
import interactive_map
import os


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
			route[n]["no data"]=False
		else:
			route[n]["no data"]= True
	final_route = []
	for i in route:
		if not i["no data"]:
			final_route.append(i)
	killed_route = []
	for i in route:
		if i not in final_route:
			killed_route.append(i)
	print("Analyse postitions of trams...")
	results = []
	for n, i in enumerate(stations):
		if n<=len(stations)-2:
			if i[0].time > stations[n+1][0].time:
				results.append([final_route[n], final_route[n+1]])
	return [final_route, results, stations, killed_route, route]

def load_observation(route_id, destination1, destination2, map_style, filename):
	answer = find_trams(str(route_id), destination1, destination2)
	map = interactive_map.Map(answer[0], map_style, [49.00994599, 8.39640733])
	map.render_marker(answer[2])
	for i in answer[3]:
		map.render_single_marker(i, color = "#aaa")
	positions = []
	for i in answer[4]:
		positions.append([i["lat"],i["lon"]])
	map.render_poly_paths(positions, color="#03f")
	for i in answer[1]:
		map.render_color_paths([i[0]["lat"],i[0]["lon"]], [i[1]["lat"],i[1]["lon"]], "#f00")
		print("Bahn zwischen", i[0]["name"], "und", i[1]["name"])
	map.save(filename)





if __name__ == '__main__':
	try:
		while True:
			load_observation(3, "Tivoli über Hbf", "Tivoli", "CartoDB Positron", "map_int.html")
			print("Wait for refresh...")
			time.sleep(30)
			os.system("cls")
	except KeyboardInterrupt as e:
		exit()

