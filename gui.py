import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class SSAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SSA Agent – Monitor kolizji satelitów")
        self.root.geometry("450x300")
        self.root.resizable(False, False)

        self.status_label = tk.Label(root, text="Status: Nierozpoczęto", font=("Arial", 12), wraplength=400)
        self.status_label.pack(pady=20)

        self.check_btn = tk.Button(root, text="Uruchom analizę TLE", command=self.run_analysis, width=30)
        self.check_btn.pack(pady=10)

        self.log_btn = tk.Button(root, text="Pokaż log z ostrzeżeniami", command=self.show_log, width=30)
        self.log_btn.pack(pady=10)

        self.quit_btn = tk.Button(root, text="Zamknij", command=self.root.quit, width=30)
        self.quit_btn.pack(pady=10)

    def run_analysis(self):
        self.status_label.config(text="Status: Trwa analiza...")
        try:
            subprocess.run(["python3", "main.py"], check=True)
            self.status_label.config(text="Status: Analiza zakończona – sprawdź log.")
        except subprocess.CalledProcessError:
            self.status_label.config(text="Status: Błąd podczas uruchamiania analizy.")
            messagebox.showerror("Błąd", "Nie udało się uruchomić analizy.")

    def show_log(self):
        log_path = "logs/alerts.log"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                log = f.read()
            if not log.strip():
                messagebox.showinfo("Log", "Brak ostrzeżeń w logu.")
            else:
                messagebox.showinfo("Log z ostrzeżeniami", log[-2000:] if len(log) > 2000 else log)
        else:
            messagebox.showwarning("Brak pliku logu", "Nie znaleziono pliku: logs/alerts.log")

def launch_gui():
    root = tk.Tk()
    app = SSAGUI(root)
    root.mainloop()