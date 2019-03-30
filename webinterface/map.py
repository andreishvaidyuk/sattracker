import folium

# Create map object
map = folium.Map(location=[51.076597, 71.383393], zoom_start=3)

# Global tooltip
tooltip = "Click me"

# Create custom marker icon
antennaIcon = folium.features.CustomIcon('images\\antenna.png', icon_size=(25, 25))
satelliteIcon = folium.features.CustomIcon('images\\satellite.png', icon_size=(25, 25))


# Create Markers
folium.Marker(location=[55.106597, 77.423393],
              popup='<strong>Location One</strong>',
              tooltip=tooltip).add_to(map)
folium.Marker(location=[51.076597, 71.383393],
              popup='<strong>Ghalam LLP</strong>',
              tooltip=tooltip,
              icon=antennaIcon).add_to(map)
folium.Marker(location=[60.076597, 82.383393],
              popup='<strong>Location Three</strong>',
              tooltip=tooltip,
              icon=satelliteIcon).add_to(map)

# Generate Map
map.save("map.html")
