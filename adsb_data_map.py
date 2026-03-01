import pandas as pd
import folium
from matplotlib import cm, colors

# CSV mit allen Live-Daten einlesen
df = pd.read_csv("adsb_live_log.csv")

# Receiver-Koordinaten für initiale Kartenansicht
receiver_lat, receiver_lon = 50.38133, 10.10459

# Karte erstellen
m = folium.Map(location=[receiver_lat, receiver_lon], zoom_start=8)

# Marker-Größe
marker_radius = 2  # sehr kleine Punkte, da viele Punkte

# Farbskala nach Höhe
color_map = cm.get_cmap('plasma_r')  # invertiert: niedrig = rot, hoch = lila
min_height = df['altitude_ft'].min()
max_height = df['altitude_ft'].max()

def height_to_color(height):
    if pd.isna(height):
        return '#808080'  # Grau für unbekannte Höhe
    norm_height = (height - min_height) / (max_height - min_height)
    rgb = color_map(norm_height)[:3]
    return colors.rgb2hex(rgb)

# Alle Punkte auf der Karte hinzufügen
for idx, row in df.iterrows():
    lat = row['lat']
    lon = row['lon']
    altitude = row['altitude_ft']
    folium.CircleMarker(
        location=[lat, lon],
        radius=marker_radius,
        color=height_to_color(altitude),
        fill=True,
        fill_color=height_to_color(altitude),
        fill_opacity=0.7
    ).add_to(m)

# Karte speichern
m.save("adsb_live_points.html")
print("Karte gespeichert: adsb_live_points.html")