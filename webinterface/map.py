import folium

map_simu = folium.Map(location=[51.076597, 71.383393], zoom_start=3, tiles="Mapbox bright")

folium.Marker(location=[51.076597, 71.383393], popup="Google HQ", icon=folium.Icon(color='gray')).add_to(map_simu)

map_simu.save("map.html")
