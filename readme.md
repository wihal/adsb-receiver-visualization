

# ADS-B Receiver Visualisierung

Dieses Projekt ermöglicht die **Analyse und Visualisierung von ADS-B-Flugdaten**, die von einem lokalen ADS-B-Receiver (z. B. Dump1090 auf einem Raspberry Pi) empfangen werden. Ziel ist es, **Flugbewegungen, Reichweite und Flughöhen** anschaulich auf Karten darzustellen.

## Projektübersicht

1. **Datenaufzeichnung**

    * Live-Daten von Dump1090 werden über TCP (`raspberrypi.local:30003`) erfasst.
    * Gespeichert werden `icao`, `callsign`, `lat`, `lon`, `altitude_ft`, `distance_km`, `timestamp`.
    * Output: **`adsb_live_log.csv`**

2. **Erste und letzte Position pro Flugzeug**

    * Aus der Live-Log-Datei wird für jedes Flugzeug der **erste und letzte empfangene Punkt** extrahiert.
    * Output: **`adsb_first_last.csv`**

3. **Visualisierung**

    * **Erste und letzte Punkte** als kleine Marker auf der Karte

      * Grün = erster Punkt
      * Rot = letzter Punkt
    * **Linien zwischen erster und letzter Position**

      * Linienfarbe zeigt Flughöhe (Rot = niedrig, Lila = hoch)
    * Kartenoutput:

      * **`adsb_first_last_lines.html`** → einfache Linienkarte
      * **`adsb_first_last_lines_colored.html`** → Linien farbcodiert nach Höhe
      * **`adsb_live_points.html`** → alle empfangenen Punkte als Marker

Hinweis: Dieses Projekt sowie die Anleitung wurden mit Unterstützung von KI erstellt und verbessert.