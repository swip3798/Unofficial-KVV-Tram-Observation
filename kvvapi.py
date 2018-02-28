import requests
from datetime import datetime,timedelta
import time
import re
import json
import re
import sys
from time import mktime


API_KEY = "377d840e54b59adbe53608ba1aad70e8"
API_BASE = "https://live.kvv.de/webapp/"
DEPARTURE_BASE = "departures/bystop/"
SEARCH_BASE = "stops/byname/"
SEARCH_STOP_BASE ="stops/bystop/"

class Departure(object):
	def __init__(self, route, destination, direction, time, lowfloor, realtime, traction, stopPosition, stop_id):
		self.route = route
		self.destination = destination
		self.direction = direction
		self.time = self._str_to_time(time)
		self.strtime = time
		self.lowfloor = lowfloor
		self.realtime = realtime
		self.traction = traction
		self.stopPosition = stopPosition
		self.stop_id = stop_id
	def _str_to_time(self, timestr):
		dt = datetime.now()

		# "0" ("sofort")
		if timestr == "0":
			return time.mktime(dt.timetuple())

		# "5 min"
		re_min = re.compile("^([1-9]) min$")
		match = re_min.match(timestr)
		if match:
			dt += timedelta(minutes=int(match.group(1)))
			return time.mktime(dt.timetuple())

		# 14:23
		re_time = re.compile("^([0-2]?[0-9]):([0-5][0-9])$")
		match = re_time.match(timestr)
		if match:
			hours = int(match.group(1))
			mins = int(match.group(2))
			time_new = dt.replace(hour=hours, minute=mins)
			if time_new < dt:
				time_new += timedelta(days=1)
			dt = time_new
			return time.mktime(dt.timetuple())
	@staticmethod
	def from_json(json):
		return Departure(json["route"], json["destination"], json["direction"], json["time"], json["lowfloor"], json["realtime"], json["traction"], json["stopPosition"], json["stop_id"])


class 	Stop(object):
	def __init__(self, name, stop_id, lat, lon):
		self.name = name
		self.stop_id = stop_id
		self.lat = lat
		self.lon = lon

	@staticmethod
	def from_json(json):
		return Stop(json["name"], json["id"], json["lat"], json["lon"])


def get_departures(stop_id):
	url = API_BASE + DEPARTURE_BASE + stop_id + "?maxInfos=30&key=" + API_KEY
	data = json.loads(requests.get(url).text)
	dep = []
	for i in data["departures"]:
		i["stop_id"] = data["stopName"]
		dep.append(Departure.from_json(i))
	return dep

def search_stop(name):
	url = API_BASE + SEARCH_BASE + name + "?key=" + API_KEY
	try:
		data = json.loads(requests.get(url).text)
		stops = []
		for i in data["stops"]:
			stops.append(Stop.from_json(i))
		return stops
	except:
		return None

def get_stop_by_id(stop_id):
	url = API_BASE + SEARCH_STOP_BASE + stop_id + "?key=" + API_KEY
	try:
		data = json.loads(requests.get(url).text)
		return Stop(name = data["name"], stop_id = data["id"], lat = data["lat"], lon = data["lon"])
	except Exception as e:
		return None


if __name__ == '__main__':
	answer = get_departures("de:8212:31")
	for i in answer:
		print(i.route, i.destination, i.time, i.strtime)