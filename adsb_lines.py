import pandas as pd
import folium

# CSV mit ersten und letzten Punkten einlesen
df = pd.read_csv("adsb_first_last.csv")

# Receiver-Koordinaten für initiale Kartenansicht
receiver_lat, receiver_lon = 50.38133, 10.10459

# Karte erstellen
m = folium.Map(location=[receiver_lat, receiver_lon], zoom_start=8)

# Farben
first_color = 'green'
last_color = 'red'
line_color = 'blue'

# Marker-Größe
marker_radius = 3  # kleine Punkte

for idx, row in df.iterrows():
    first_lat = row['first_lat']
    first_lon = row['first_lon']
    last_lat = row['last_lat']
    last_lon = row['last_lon']

    # Erster Punkt (grün)
    folium.CircleMarker(
        location=[first_lat, first_lon],
        radius=marker_radius,
        color=first_color,
        fill=True,
        fill_color=first_color,
        fill_opacity=1
    ).add_to(m)

    # Letzter Punkt (rot)
    folium.CircleMarker(
        location=[last_lat, last_lon],
        radius=marker_radius,
        color=last_color,
        fill=True,
        fill_color=last_color,
        fill_opacity=1
    ).add_to(m)

    # Linie zwischen erster und letzter Position
    folium.PolyLine(
        locations=[[first_lat, first_lon], [last_lat, last_lon]],
        color=line_color,
        weight=1,
        opacity=0.7
    ).add_to(m)

# Karte speichern
m.save("adsb_first_last_lines.html")
print("Karte gespeichert: adsb_first_last_lines.html")