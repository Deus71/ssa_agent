import requests
import datetime
from secrets import SPACETRACK_USER, SPACETRACK_PASS
import yaml
import os

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def login_space_track():
    session = requests.Session()
    login_url = "https://www.space-track.org/ajaxauth/login"
    credentials = {
        "identity": SPACETRACK_USER,
        "password": SPACETRACK_PASS
    }
    session.post(login_url, data=credentials)
    return session

def fetch_tle(session, norad_id):
    url = f"https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/{norad_id}/orderby/epoch desc/limit/1/format/tle"
    r = session.get(url)
    return r.text.strip()

def fetch_all_tle():
    config = load_config()
    session = login_space_track()

    all_tle = ""
    for sat in config['satellites']:
        tle = fetch_tle(session, sat['norad_id'])
        all_tle += f"# {sat['name']} ({sat['norad_id']})\n{tle}\n\n"

    os.makedirs("data", exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M")
    with open("data/tle_current.txt", "w") as f:
        f.write(all_tle)
    print(f"[INFO] Zapisano TLE do data/tle_current.txt")

if __name__ == "__main__":
    fetch_all_tle()
