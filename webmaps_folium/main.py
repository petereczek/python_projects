#Application that prompts user for file and creates a webmap with inputted locations from a chosen file.

import folium 
import pandas as pd

filename = str(input("Please enter filename containing list of locations and their names to place on webmap:"))

if filename.endswith(".json"):
	data = pd.read_json(filename)
elif filename.endswith('.xlsx'):
	data = pd.read_excel(filename)
elif filename.endswith(('.txt', '.csv')):
	data = pd.read_csv(filename)

lats = list(data['LAT'])
lons = list(data['LON'])
names = list(data['NAME'])
elev = list(data['ELEV'])

#Creating dynamic coloring function to signify magnitude of range for points on map. This case is for elevation parameter, but can be customized to others. Generates color to be used when adding markers.

def dynamic_color(elev):
	if elev >0 and elev <= 1000:
		return 'green'
	elif elev > 1000 and elev<=2000:
		return 'yellow'
	elif elev > 2000 and elev <= 3500:
		return 'orange'
	elif elev > 3500:
		return 'red'


#Creating webmap with folium

map = folium.Map(location = [40.7128, -74.0060], zoom_start = 6, tiles = "Mapbox Bright")

fg = folium.FeatureGroup(name = "mapfeatures")

for lat, lon, name, el in zip(lats, lons, names, elev):
	fg.add_child(folium.CircleMarker(location = [lat,lon], popup = name+', elevation: '+str(el)+'m', fill_color = dynamic_color(el), color= 'grey', fill_opacity = 0.5))
fg.add_child(folium.GeoJson(data = open("world.json",encoding = 'utf-8-sig').read()))
map.add_child(fg)
map.add_child(folium.LayerControl())
map.save("Map.html")

print("Map ready. Open file Map.html in your browser!")
