from __future__ import print_function
import builtins
import kvvapi
import requests
import json
import time
import interactive_map
import os
import sys
import ftpupload


def print(*args, **kwargs):
	formatted_time = time.ctime()
	output_str = "[" + formatted_time + "] "
	for i in args:
		output_str += str(i) + " "
	with open("output.log", "a") as f:
		f.write(output_str + "\n")
	builtins.print(output_str)


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

def load_observation(route_id, destination1, destination2, map_style, filename, destinationlist = [], zoom = 13.4):
	answer = find_trams(str(route_id), destination1, destination2, destinationlist = destinationlist)
	middle = answer[4][int(len(answer[4])/2)]
	map = interactive_map.Map(answer[0], map_style, [middle["lat"], middle["lon"]], zoom_start = zoom)
	map.render_marker(answer[2])
	for i in answer[3]:
		map.render_single_marker(i, color = "#aaa")
	positions = []
	for i in answer[4]:
		positions.append([i["lat"],i["lon"]])
	map.render_poly_paths(positions, color="#03f")
	for i in answer[1]:
		map.render_color_paths([i[0]["lat"],i[0]["lon"]], [i[1]["lat"],i[1]["lon"]], "#f00",i[1]["depar"][0].route + " " + i[1]["depar"][0].destination)
		print("Bahn zwischen", i[0]["name"], "und", i[1]["name"])
	map.save(filename)





if __name__ == '__main__':
	os.system("cls")
	while True:
		try:
			while True:
				try:
					load_observation(3, "Tivoli über Hbf", "Tivoli", "CartoDB Positron", "map_3_tivoli.html")
					load_observation(3, "Heide", "Heide", "CartoDB Positron", "map_3_heide.html")
					load_observation("S4", "Karlsruhe Hbf", "Karlsruhe Hbf", "CartoDB Positron", "map_s4_karlsruhe.html", ["Karlsruhe Albtalbahnhof"], 11)
					load_observation("S4", "Heilbronn Hbf", "Heilbronn Pfühlpark", "CartoDB Positron", "map_s4_heilbronn.html", ["Öhringen Cappel EILZUG", "Flehingen", "Weinsberg", "Heilbronn Pfühlpark", "Bretten Gölshausen"], 11)
				except Exception as e:
					print("Error ", e, "was raised on script execution")
				print("Upload maps...")
				try:
					ftpupload.uploadFile(".ftpurl", ".user", ".pass", [["map_3_heide.html","KVV/map_3_heide.html"],["map_3_tivoli.html","KVV/map_3_tivoli.html"],["map_s4_heilbronn.html", "KVV/map_s4_heilbronn.html"], ["map_s4_karlsruhe.html", "KVV/map_s4_karlsruhe.html"]])
				except Exception as e:
					print("No upload was possible", e)
				print("Wait for refresh...")
				time.sleep(15)
		except KeyboardInterrupt as e:
			continue
		except Exception as e:
			print(e, "was raised and killed the script")
			exit()

