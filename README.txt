SSA_AGENT - lokalny agent monitorujący zmiany orbit satelitów

1. Uzupełnij dane logowania do Space-Track.org w pliku secrets.py.
2. Uruchom środowisko virtualenv.
3. Zainstaluj wymagane biblioteki: pip install -r requirements.txt
4. Uruchom agenta: python main.py

Zostanie pobrany aktualny TLE i zapisany do pliku data/tle_current.txt.
Poprzedni TLE zostanie zarchiwizowany jako data/tle_previous.txt.
