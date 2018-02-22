import requests
from datetime import datetime,timedelta
import re
import json
import re
import sys


API_KEY = "377d840e54b59adbe53608ba1aad70e8"
API_BASE = "https://live.kvv.de/webapp/"

class Departures(object):
	def __init__(self, route=None, destination=None, direction=None, time=None, lowfloor=None, realtime=None, traction=None, stopPosition=None, json_text=None):
		if json_text==None:
			self.route = route
			self.destination = destination
			self.direction = direction
			self.time = time
			self.lowfloor = lowfloor
			self.realtime = realtime
			self.traction = traction
			self.stopPosition = stopPosition
		else:

		print(time)
	def 