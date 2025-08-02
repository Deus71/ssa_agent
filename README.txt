SSA Agent – System Ostrzegania przed Kolizjami Satelitów
==========================================================

Opis:
-----
Program analizuje dane TLE (Two-Line Element) satelitów w celu wykrycia potencjalnych kolizji na orbicie. 
Działa zarówno w trybie porównywania wskazanych obiektów, jak i analizie all-to-all.

Wymagania:
----------
- Python 3.10+
- Połączenie z Internetem
- Zainstalowane biblioteki z `requirements.txt`
- Konto na Space-Track.org (opcjonalne, ale zalecane)

Uruchomienie:
-------------
1. Aktywuj środowisko:
   $ source venv/bin/activate

2. Uruchom GUI:
   $ python3 start_gui.py

Ustawienia w GUI:
-----------------
1. **Wybór trybu analizy**:
   - 'Porównaj wskazany satelita z grupą' – wybiera obiekt z `config.yaml`
   - 'All-to-All' – porównuje wszystkie obiekty między sobą

2. **Źródło danych TLE**:
   - active (aktywne satelity)
   - debris (kosmiczne śmieci)
   - starlink (konstelacja Starlink)
   - custom (inne – jeśli dodane w kodzie)

3. **Zapis ustawień**:
   - Wybrane opcje są zapisywane do `config.yaml`.

4. **Źródło danych TLE (priorytet)**:
   - Space-Track.org (jeśli login/hasło obecne w `secrets.py`)
   - W razie błędu – fallback do Celestrak

5. **Dziennik komunikatów**:
   - Komunikaty zapisywane są w `log.txt`
   - W przypadku wykrycia zbliżeń, pojawią się wpisy z czasem, nazwami obiektów i dystansem

Konfiguracja:
-------------
Plik `config.yaml` zawiera:
- monitored_satellites: lista satelitów (dla trybu selektywnego)
- tle_source: jedno ze źródeł TLE (active.txt, debris.txt itd.)
- check_mode: 'selected' lub 'all'

Dane logowania:
---------------
Plik `secrets.py` musi zawierać:
```python
SPACE_TRACK_USER = 'your_username'
SPACE_TRACK_PASS = 'your_password'
```

Uwaga:
------
- Dane TLE są analizowane dla najbliższych 6 godzin w krokach co 10 minut.
- Możliwe chwilowe błędy po stronie Space-Track (kod 500).
- W razie problemów – użyj alternatywnego źródła Celestrak.

Autor: Tadeusz Polanowski
<<<<<<< HEAD
Data: Lipiec 2025
=======
Data: Lipiec 2025
>>>>>>> 872881a7faea43b2a9f56ee36e514bdc6ffebf70
