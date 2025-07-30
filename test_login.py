import requests
from secrets import SPACETRACK_USER, SPACETRACK_PASS

def test_space_track_login():
    login_url = "https://www.space-track.org/ajaxauth/login"
    credentials = {
        "identity": SPACETRACK_USER,
        "password": SPACETRACK_PASS
    }

    with requests.Session() as session:
        response = session.post(login_url, data=credentials)

        if response.status_code == 200 and "Set-Cookie" in response.headers:
            print("[✅] Logowanie zakończone sukcesem.")
        else:
            print(f"[❌] Logowanie nie powiodło się. Kod odpowiedzi: {response.status_code}")
            print("Treść odpowiedzi:", response.text)

if __name__ == "__main__":
    test_space_track_login()
