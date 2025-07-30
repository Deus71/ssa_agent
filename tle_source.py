import requests
import urllib3
import base64
from secrets import SPACETRACK_USER, SPACETRACK_PASS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_tle_from_celestrak(group):
    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"
    try:
        r = requests.get(url, timeout=20, verify=False)
        if r.status_code == 200:
            print(f"[INFO] Dane TLE pobrane z Celestrak – grupa: {group}")
            return r.text.strip()
        else:
            print(f"[ERROR] Celestrak zwrócił kod {r.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Błąd połączenia z Celestrak: {e}")
        return None

def fetch_tle_from_spacetrack(group):
    login_url = "https://www.space-track.org/ajaxauth/login"
    query_url = f"https://www.space-track.org/basicspacedata/query/class/tle_latest/format/tle/group/{group}"

    try:
        session = requests.Session()
        login_data = {
            "identity": SPACETRACK_USER,
            "password": SPACETRACK_PASS
        }
        r = session.post(login_url, data=login_data, timeout=20)
        if r.status_code != 200:
            print(f"[ERROR] Logowanie do Space-Track nie powiodło się: {r.status_code}")
            return None
        r = session.get(query_url, timeout=30)
        if r.status_code == 200:
            print(f"[INFO] Dane TLE pobrane z Space-Track – grupa: {group}")
            return r.text.strip()
        else:
            print(f"[ERROR] Space-Track zwrócił kod {r.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Błąd pobierania z Space-Track: {e}")
        return None

def fetch_tle(config):
    provider = config.get("tle_provider", "celestrak")
    group = config.get("tle_group", "active")
    if provider == "spacetrack":
        return fetch_tle_from_spacetrack(group)
    else:
        return fetch_tle_from_celestrak(group)