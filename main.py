from __future__ import print_function
import builtins
import kvvapi
import requests
import json
import time
import interactive_map
import os
import sys
import logging
import ftpupload


def print(*args, **kwargs):
	formatted_time = time.ctime()
	output_str = formatted_time + ": "
	for i in args:
		output_str += str(i)
	with open("output.log", "a") as f:
		f.write(output_str)
	builtins.print(formatted_time  + ": ", *args, **kwargs)


def find_trams(route_id, destination1, destination2, destinationlist = []):
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
			if i.route == str(route_id) and (i.destination == destination or destination_file == i.destination or i.destination in destinationlist):
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

def load_observation(route_id, destination1, destination2, map_style, filename, destinationlist = []):
	answer = find_trams(str(route_id), destination1, destination2, destinationlist = destinationlist)
	map = interactive_map.Map(answer[0], map_style, [49.0177632, 8.3850749])
	map.render_marker(answer[2])
	for i in answer[3]:
		map.render_single_marker(i, color = "#aaa")
	positions = []
	for i in answer[4]:
		positions.append([i["lat"],i["lon"]])
	map.render_poly_paths(positions, color="#03f")
	for i in answer[1]:
		map.render_color_paths([i[0]["lat"],i[0]["lon"]], [i[1]["lat"],i[1]["lon"]], "#f00", i[1]["depar"][0].destination)
		print("Bahn zwischen", i[0]["name"], "und", i[1]["name"])
		logger.info("Tram found between %s and %s", i[0]["name"], i[1]["name"])
	map.save(filename)





if __name__ == '__main__':
	os.system("cls")
	logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO, filename="messages.log")
	logger = logging.getLogger(__name__)
	while True:
		try:
			while True:
				try:
					load_observation(3, "Tivoli über Hbf", "Tivoli", "CartoDB Positron", "map_3_tivoli.html")
					load_observation(3, "Heide", "Heide", "CartoDB Positron", "map_3_heide.html")
					load_observation("S4", "Karlsruhe Hbf", "Karlsruhe Hbf", "CartoDB Positron", "map_s4_karlsruhe.html", ["Karlsruhe Albtalbahnhof"])
					load_observation("S4", "Heilbronn Hbf", "Heilbronn Pfühlpark", "CartoDB Positron", "map_s4_heilbronn.html", ["Öhringen Cappel EILZUG", "Flehingen", "Weinsberg", "Heilbronn Pfühlpark", "Bretten Gölshausen"])
					logger.info("Full script execution was managed")
				except Exception as e:
					logger.info("Error %s was raised on script execution, retry in 30 sec...", str(e))
					print("Error ", e, "was raised on script execution")
				print("Upload maps...")
				try:
					ftpupload.uploadFile(".ftpurl", ".user", ".pass", [["map_3_heide.html","KVV/map_3_heide.html"],["map_3_tivoli.html","KVV/map_3_tivoli.html"]])
				except:
					print("no upload")
				print("Wait for refresh...")
				time.sleep(30)
		except KeyboardInterrupt as e:
			continue
		except Exception as e:
			logger.info("%s was raised and killed the script", str(e))
			exit()

