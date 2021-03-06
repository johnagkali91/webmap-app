import folium
import pandas
import numpy
data = pandas.read_csv("Volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
loc = list(data["LOCATION"])

html = """
Volcano information:
<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a>
<br>
Location: %s
<br>
Height: %s m
"""


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[numpy.mean(lat), numpy.mean(lon)], zoom_start=4, tiles="OpenStreetMap")

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=(lambda x:{'fillColor':'green' if x['properties']['POP2005'] <20000000
else  'yellow' if 20000000 <= x['properties']['POP2005'] <80000000
else 'red'} )))

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, name, loc in zip(lat, lon, elev, name, loc):
    iframe = folium.IFrame(html=html % (name, name,loc, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=folium.Popup(iframe),
    fill_color=color_producer(el), color='grey', fill_opacity=0.7))



map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
