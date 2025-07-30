import tkinter as tk
from tkinter import ttk, messagebox
import yaml
from tle_source import fetch_tle
from proximity_checker import run_proximity_check

CONFIG_FILE = "config.yaml"
AVAILABLE_GROUPS = [
    "active", "stations", "visual", "weather", "resource", "science", "geodetic",
    "engineering", "military", "communication", "navigation", "starlink"
]

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        yaml.dump(config, f, sort_keys=False)

def run_analysis():
    config["selected_mode"] = mode_var.get()
    config["selected_satellite"] = satellite_var.get()
    config["tle_provider"] = provider_var.get()
    config["tle_group"] = group_var.get()
    save_config(config)

    tle_text = fetch_tle(config)
    if not tle_text:
        messagebox.showerror("Błąd", "Nie udało się pobrać danych TLE.")
        return

    run_proximity_check(tle_text, config)
    messagebox.showinfo("Zakończono", "Analiza zakończona. Sprawdź logi.")

config = load_config()

root = tk.Tk()
root.title("SSA – Analiza TLE")
root.geometry("420x300")

# Satelita
tk.Label(root, text="Wybierz satelitę:").pack()
satellite_var = tk.StringVar(value=config.get("selected_satellite", "All-to-All"))
satellite_list = [s["name"] for s in config["satellites"]]
satellite_menu = ttk.Combobox(root, textvariable=satellite_var, values=satellite_list + ["All-to-All"])
satellite_menu.pack()

# Tryb analizy
tk.Label(root, text="Tryb analizy:").pack()
mode_var = tk.StringVar(value=config.get("selected_mode", "all_to_all"))
mode_menu = ttk.Combobox(root, textvariable=mode_var, values=["all_to_all", "one_vs_all"])
mode_menu.pack()

# Provider
tk.Label(root, text="Źródło danych TLE:").pack()
provider_var = tk.StringVar(value=config.get("tle_provider", "celestrak"))
provider_menu = ttk.Combobox(root, textvariable=provider_var, values=["celestrak", "spacetrack"])
provider_menu.pack()

# Grupa obiektów
tk.Label(root, text="Grupa obiektów:").pack()
group_var = tk.StringVar(value=config.get("tle_group", "active"))
group_menu = ttk.Combobox(root, textvariable=group_var, values=AVAILABLE_GROUPS)
group_menu.pack()

# Start
tk.Button(root, text="Uruchom analizę", command=run_analysis).pack(pady=10)

root.mainloop()