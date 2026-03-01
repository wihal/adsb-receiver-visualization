# ADS-B Receiver Visualization

This project enables the **analysis and visualization of ADS-B flight data** received by a local ADS-B receiver (e.g., Dump1090 on a Raspberry Pi). The goal is to clearly display **flight movements, range, and flight altitudes** on maps.

## Project Overview

1. **Data Recording**

* Live data from Dump1090 is captured via TCP (`raspberrypi.local:30003`).
* The following data is stored: `icao`, `callsign`, `lat`, `lon`, `altitude_ft`, `distance_km`, `timestamp`.
    * Output: **`adsb_live_log.csv`**

2. **First and last position per aircraft**

* The **first and last received point** for each aircraft is extracted from the live log file.
* Output: **`adsb_first_last.csv`**

3. **Visualization**
    * **First and last points** as small markers on the map
      * Green = first point
      * Red = last point
* **Lines between first and last position**
      * Line color indicates flight altitude (red = low, purple = high)
* Map output:
  * **`adsb_first_last_lines.html`** → simple line map
  * **`adsb_first_last_lines_colored.html`** → lines color-coded by altitude
  * **`adsb_live_points.html`** → all received points as markers


Note: This project and the instructions were created and improved with the support of AI.
