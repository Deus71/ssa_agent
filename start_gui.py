import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import yaml
from fpdf import FPDF
from datetime import datetime
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

    log_lines = run_proximity_check(tle_text, config)

    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_path = f"logs/ssa_log_{now}.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"[INFO] Analiza przeprowadzona: {now}\n")
        f.write("[INFO] Dane TLE pobrane i sprawdzone.\n\n")
        for line in log_lines:
            f.write(line + "\n")

    messagebox.showinfo("Zakończono", f"Analiza zakończona.\nZapisano log:\n{log_path}")


def show_log_window():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        messagebox.showwarning("Brak katalogu", f"Nie znaleziono katalogu logów: {log_dir}")
        return

    log_files = [f for f in os.listdir(log_dir) if f.startswith("ssa_log_") and f.endswith(".txt")]
    if not log_files:
        messagebox.showwarning("Brak plików", "Brak zapisanych logów do wyświetlenia.")
        return

    latest_log = max(log_files)
    log_path = os.path.join(log_dir, latest_log)

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    log_window = tk.Toplevel()
    log_window.title(f"Ostatni log: {latest_log}")
    log_window.geometry("800x550")

    text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Courier", 10))
    text_area.insert(tk.END, content)
    text_area.configure(state='disabled')
    text_area.pack(expand=True, fill='both')

    def save_as_txt():
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Plik tekstowy", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Zapisano", f"Log zapisany jako:\n{path}")

    def save_as_pdf():
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Plik PDF", "*.pdf")])
        if path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Courier", size=10)
            for line in content.splitlines():
                pdf.cell(0, 5, txt=line[:100], ln=1)
            pdf.output(path)
            messagebox.showinfo("Zapisano", f"Log zapisany jako:\n{path}")

    btn_frame = tk.Frame(log_window)
    btn_frame.pack(pady=10)

    btn_txt = tk.Button(btn_frame, text="💾 Zapisz jako .txt", command=save_as_txt)
    btn_txt.pack(side=tk.LEFT, padx=10)

    btn_pdf = tk.Button(btn_frame, text="🖨️ Zapisz jako .pdf", command=save_as_pdf)
    btn_pdf.pack(side=tk.LEFT, padx=10)


config = load_config()

root = tk.Tk()
root.title("SSA – Analiza TLE")
root.geometry("420x360")

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

# Start analizy
tk.Button(root, text="Uruchom analizę", command=run_analysis).pack(pady=10)

# Pokaż log
tk.Button(root, text="📄 Pokaż ostatni log", command=show_log_window).pack(pady=5)

root.mainloop()
