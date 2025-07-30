import os
from sgp4.api import Satrec
from sgp4.api import jday

def parse_tle_block(tle_text):
    blocks = tle_text.strip().split("\n\n")
    satellites = {}
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) == 3:
            name_line = lines[0]
            line1 = lines[1].strip()
            line2 = lines[2].strip()
            name = name_line.replace("#", "").strip()
            satellites[name] = (line1, line2)
    return satellites

def compare_tle_sets(prev, curr, threshold_deg=0.01):
    alerts = []
    for name in curr:
        if name in prev:
            s1 = Satrec.twoline2rv(*prev[name])
            s2 = Satrec.twoline2rv(*curr[name])

            d_inclination = abs(s1.inclo - s2.inclo) * (180 / 3.1415926535)  # rad to deg
            d_raan = abs(s1.nodeo - s2.nodeo) * (180 / 3.1415926535)  # rad to deg

            if d_inclination > threshold_deg or d_raan > threshold_deg:
                alerts.append(f"[ALERT] {name}: ΔIncl={d_inclination:.4f}°, ΔRAAN={d_raan:.4f}°")

    return alerts

def run_orbit_change_detection():
    if not os.path.exists("data/tle_previous.txt") or not os.path.exists("data/tle_current.txt"):
        print("[WARN] Brakuje plików TLE do porównania.")
        return

    with open("data/tle_previous.txt") as f:
        prev_tle = parse_tle_block(f.read())

    with open("data/tle_current.txt") as f:
        curr_tle = parse_tle_block(f.read())

    alerts = compare_tle_sets(prev_tle, curr_tle)

    if alerts:
        with open("logs/alerts.log", "a") as log:
            for alert in alerts:
                print(alert)
                log.write(alert + "\n")
    else:
        print("[INFO] Brak istotnych zmian orbit.")
