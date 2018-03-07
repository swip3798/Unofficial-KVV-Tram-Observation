import folium
import re
import json
import scipy



class Map(object):
	def __init__(self, loc_data, tiles, location, zoom_start = 13.4):
		self.map = folium.Map(location = location,
								zoom_start = zoom_start,
								tiles=tiles)
		self.loc_data = loc_data
	def render_marker(self, infos, color = "#03f"):
		for n, i in enumerate(self.loc_data):
			self.loc_data[n]["depar"] = infos[n]
		for n, i in enumerate(self.loc_data):
			popup_text = i["name"] + "<br>"
			for j in i["depar"]:
				popup_text += j.route + " " + j.destination + " " + j.strtime + "<br>"
			popup_text = re.escape(popup_text)
			marker = folium.CircleMarker(location = [i["lat"], i["lon"]], popup = popup_text, fill = True, radius = 8, color = color)
			marker.add_to(self.map)
	def render_poly_paths(self, positions, color):
		lines = folium.PolyLine(positions, color = color)
		lines.add_to(self.map)
	def render_color_paths(self, location1, location2, color, popup = None):
		line = folium.PolyLine([location1, location2], color = color, popup = popup)
		line.add_to(self.map)
	def render_single_marker(self, location, color = "#03f", radius = 8):
		popup_text = location["name"] + "<br>"
		popup_text = re.escape(popup_text)
		marker = folium.CircleMarker(location = [location["lat"], location["lon"]], popup = popup_text, fill = True, radius = radius, color = color)
		marker.add_to(self.map)

	def save(self, filename):
		self.map.save(filename)



		

def createInteractiveMap(data, filename, tiles):
	folium_map = folium.Map(location=[25, 0],
							zoom_start=3,
							tiles=tiles)
	print("Add stuff")
	for i in data:
		popup_text = i["name"]
		popup_text = re.escape(popup_text)
		marker = folium.CircleMarker(location=[i["lat"], i["lon"]], popup=popup_text, fill=True, radius = 5)
		marker.add_to(folium_map)
	
	print("save")
	folium_map.save(filename)


if __name__ == '__main__':
	pass