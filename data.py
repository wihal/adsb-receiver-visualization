import socket
import pandas as pd
from math import radians, sin, cos, sqrt, asin
import time

# Receiver-Koordinaten
receiver_lat, receiver_lon = 0, 0

# Haversine-Funktion zur Entfernungsmessung
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Erdradius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*R*asin(sqrt(a))

# TCP-Verbindung zu Dump1090
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("raspberrypi.local", 30003))
print("Verbunden zu Dump1090 auf raspberrypi.local:30003")

# CSV-Datei vorbereiten
csv_file = "adsb_live_log.csv"

# Daten sammeln
data = []

try:
    for _ in range(100000):
        print(_)
        line = s.recv(1024).decode('utf-8', errors='ignore').strip()
        for msg in line.split('\n'):
            fields = msg.split(',')
            # MSG-Typ 3 = Positionsmeldung
            if len(fields) > 15 and fields[1] == '3':
                icao = fields[4]
                callsign = fields[10].strip() if fields[10] else ''  # Callsign aus MSG,3 (falls vorhanden)
                lat = fields[14]
                lon = fields[15]
                altitude = fields[11]  # Höhe in Fuß
                timestamp = fields[6]   # Zeit der Meldung

                if lat and lon:
                    try:
                        lat = float(lat)
                        lon = float(lon)
                        altitude = float(altitude) if altitude else None
                        distance = haversine(receiver_lat, receiver_lon, lat, lon)
                        data.append([icao, callsign, lat, lon, altitude, distance, timestamp])
                    except ValueError:
                        continue

        # Zwischenspeicherung in CSV alle 500 Datensätze
        if len(data) >= 500:
            df = pd.DataFrame(data, columns=['icao','callsign','lat','lon','altitude_ft','distance_km','timestamp'])
            df.to_csv(csv_file, mode='a', index=False, header=not pd.io.common.file_exists(csv_file))
            data = []

except KeyboardInterrupt:
    print("Logging beendet, speichere letzte Daten...")
    if data:
        df = pd.DataFrame(data, columns=['icao','callsign','lat','lon','altitude_ft','distance_km','timestamp'])
        df.to_csv(csv_file, mode='a', index=False, header=not pd.io.common.file_exists(csv_file))
    s.close()
    print(f"CSV gespeichert: {csv_file}")



# Eingabe-CSV
input_csv = "adsb_live_log.csv"
# Ausgabe-CSV
output_csv = "adsb_first_last.csv"

# CSV einlesen
df = pd.read_csv(input_csv)

# Nach ICAO sortieren nach Timestamp
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(['icao', 'timestamp'])

# Funktion, um ersten und letzten Punkt pro Flugzeug zu bekommen
first_last = df.groupby('icao').agg(
    first_lat=('lat', 'first'),
    first_lon=('lon', 'first'),
    first_altitude=('altitude_ft', 'first'),
    first_callsign=('callsign', 'first'),
    first_timestamp=('timestamp', 'first'),
    last_lat=('lat', 'last'),
    last_lon=('lon', 'last'),
    last_altitude=('altitude_ft', 'last'),
    last_callsign=('callsign', 'last'),
    last_timestamp=('timestamp', 'last')
).reset_index()

# CSV speichern
first_last.to_csv(output_csv, index=False)
print(f"Erste und letzte Positionen pro Flugzeug gespeichert in: {output_csv}")