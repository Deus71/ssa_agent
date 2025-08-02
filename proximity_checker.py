from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime, timedelta
from itertools import combinations
import math

def parse_tle_lines(tle_text):
    lines = tle_text.strip().split("\n")
    catalog = {}
    for i in range(0, len(lines), 3):
        name = lines[i].strip()
        line1 = lines[i+1].strip()
        line2 = lines[i+2].strip()
        sat = Satrec.twoline2rv(line1, line2)
        catalog[name] = sat
    return catalog

def distance_km(pos1, pos2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))

def run_proximity_check(tle_text, config):
    log_lines = []
    catalog = parse_tle_lines(tle_text)
    mode = config.get("selected_mode", "all_to_all")
    selected_name = config.get("selected_satellite")
    tle_group = config.get("tle_group", "unknown")
    step_minutes = 10
    threshold_km = 10
    duration_hours = 6

    now = datetime.utcnow()
    dt_range = [now + timedelta(minutes=i * step_minutes) for i in range(int(60 / step_minutes * duration_hours))]

    sat_items = list(catalog.items())
    sat_names = list(catalog.keys())

    log_lines.append(f"[INFO] Rozpoczęto analizę o {now.isoformat()} UTC")
    log_lines.append(f"[INFO] Grupa danych TLE: {tle_group}")
    log_lines.append(f"[INFO] Tryb: {mode}")
    log_lines.append(f"[INFO] Liczba satelitów: {len(sat_items)}")

    # Lista nazw satelitów (limit 15)
    max_list = 15
    log_lines.append(f"[INFO] Sprawdzane satelity:")
    for name in sat_names[:max_list]:
        log_lines.append(f" - {name}")
    if len(sat_names) > max_list:
        log_lines.append(f"[INFO] ... i {len(sat_names) - max_list} pozostałych")

    if mode == "one_vs_all" and selected_name in catalog:
        log_lines.append(f"[INFO] Obiekt bazowy: {selected_name}")
        base_sat = catalog[selected_name]
        for name, sat in sat_items:
            if name == selected_name:
                continue
            for dt in dt_range:
                jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond * 1e-6)
                _, ra = base_sat.sgp4(jd, fr)
                _, rb = sat.sgp4(jd, fr)
                d = distance_km(ra, rb)
                if d < threshold_km:
                    line = f"[WARNING] {dt.isoformat()} — {selected_name} vs {name}: distance = {d:.2f} km"
                    print(line)
                    log_lines.append(line)
    else:
        pair_count = len(sat_items) * (len(sat_items) - 1) // 2
        log_lines.append(f"[INFO] Liczba par do porównania: {pair_count}")
        for (name_a, sat_a), (name_b, sat_b) in combinations(sat_items, 2):
            for dt in dt_range:
                jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond * 1e-6)
                _, ra, _ = sat_a.sgp4(jd, fr)
                _, rb, _ = sat_b.sgp4(jd, fr)
                d = distance_km(ra, rb)
                if d < threshold_km:
                    line = f"[WARNING] {dt.isoformat()} — {name_a} vs {name_b}: distance = {d:.2f} km"
                    print(line)
                    log_lines.append(line)

    if not any("[WARNING]" in line for line in log_lines):
        log_lines.append("[INFO] Nie wykryto niebezpiecznych zbliżeń.")

    return log_lines
