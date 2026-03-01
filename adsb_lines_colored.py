import pandas as pd
import folium
from matplotlib import colors, cm

# CSV mit ersten und letzten Punkten einlesen
df = pd.read_csv("adsb_first_last.csv")

# Receiver-Koordinaten für initiale Kartenansicht
receiver_lat, receiver_lon = 50.38133, 10.10459

# Karte erstellen
m = folium.Map(location=[receiver_lat, receiver_lon], zoom_start=8)

# Marker-Größe
marker_radius = 3  # kleine Punkte

# Farben: von Rot → Lila (niedrig → hoch)
color_map = cm.get_cmap('plasma')  # Plasma verläuft von lila → gelb, wir können invertieren
# Wir invertieren, sodass Rot = niedrig, Lila = hoch
color_map = cm.get_cmap('plasma_r')  

# Höhe min/max für Normierung
min_height = df[['first_altitude', 'last_altitude']].min().min()
max_height = df[['first_altitude', 'last_altitude']].max().max()

def height_to_color(height):
    # Normierte Höhe 0..1
    norm_height = (height - min_height) / (max_height - min_height)
    rgb = color_map(norm_height)[:3]  # matplotlib gibt RGBA
    # In Hex umwandeln
    return colors.rgb2hex(rgb)

for idx, row in df.iterrows():
    first_lat = row['first_lat']
    first_lon = row['first_lon']
    last_lat = row['last_lat']
    last_lon = row['last_lon']

    # Mittelwert der Höhe für Farbgebung
    avg_height = (row['first_altitude'] + row['last_altitude']) / 2 if pd.notna(row['first_altitude']) and pd.notna(row['last_altitude']) else 0
    line_color = height_to_color(avg_height)

    # Erster Punkt (grün)
    folium.CircleMarker(
        location=[first_lat, first_lon],
        radius=marker_radius,
        color='green',
        fill=True,
        fill_color='green',
        fill_opacity=1
    ).add_to(m)

    # Letzter Punkt (rot)
    folium.CircleMarker(
        location=[last_lat, last_lon],
        radius=marker_radius,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=1
    ).add_to(m)

    # Linie zwischen erster und letzter Position mit farbverlauf
    folium.PolyLine(
        locations=[[first_lat, first_lon], [last_lat, last_lon]],
        color=line_color,
        weight=2,
        opacity=0.8
    ).add_to(m)

# Karte speichern
m.save("adsb_first_last_lines_colored.html")
print("Karte gespeichert: adsb_first_last_lines_colored.html")