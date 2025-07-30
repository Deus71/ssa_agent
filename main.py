import shutil
import os
import tle_fetcher
import orbit_change_detector
import proximity_checker

def backup_previous_tle():
    if os.path.exists("data/tle_current.txt"):
        shutil.copy("data/tle_current.txt", "data/tle_previous.txt")

if __name__ == "__main__":
    backup_previous_tle()
    tle_fetcher.fetch_all_tle()
    print("[INFO] Dane TLE zaktualizowane i gotowe do dalszej analizy.")
    orbit_change_detector.run_orbit_change_detection()
    proximity_checker.run_proximity_check()
