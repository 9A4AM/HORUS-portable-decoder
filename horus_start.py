#-------------------------------------------------------------------------------
# Name:        horus_start.py
# Purpose:
#
# Author:      9A4AM
#
# Created:     31.05.2024
# Copyright:   (c) 9A4AM 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import time
import threading
import os
import signal

# Globalna promenljiva za subprocess
process = None

def run_horus_script():
    global process
    # Pokreni horus_start.sh skriptu
    process = subprocess.Popen(['./horus_start.sh'], preexec_fn=os.setsid)

    # Pokreni proveru loga u zasebnoj niti
    threading.Thread(target=update_log).start()

def update_log():
    # Proveri log fajl periodično
    while True:
        try:
            with open('log_horus', 'r') as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]
                    # lat, lon, alt = parse_log_line(last_line)
                    # update_text(lat, lon, alt)
                    update_text(last_line)
        except FileNotFoundError:
            pass

        time.sleep(5)  # Proveravaj svakih 5 sekundi

def parse_log_line(last_line):
    # Parsiraj liniju loga i izvuci Lat, Lon, Alt
    parts = last_line.strip().split(',')
    lat = parts[0].split('=')[1]
    lon = parts[1].split('=')[1]
    alt = parts[2].split('=')[1]
    return lat, lon, alt

# def update_text(lat, lon, alt):
def update_text(last_line):
    # Ažuriraj tekstualno polje sa novim vrednostima
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    # text_widget.insert(tk.END, f"Lat: {lat}\nLon: {lon}\nAlt: {alt}")
    text_widget.insert(tk.END, f"Frequency: 437.600MHz\n Last packet:\n {last_line}\n")
    text_widget.config(state=tk.DISABLED)

def stop_horus_script():
    global process
    if process:
        # Zaustavi bash skriptu
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        time.sleep(1)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        process = None
    root.quit()

# Kreiraj Tkinter prozor
root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Horus Decoder by 9A4AM")

# Kreiraj dugme za pokretanje skripte
start_button = tk.Button(root, text="Start decoder", command=run_horus_script)
start_button.pack(pady=10)

# Kreiraj dugme za zaustavljanje skripte
stop_button = tk.Button(root, text="Stop decoder & Exit", command=stop_horus_script)
stop_button.pack(pady=10)

# Kreiraj skrolovani tekstualni widget za prikaz loga
text_widget = scrolledtext.ScrolledText(root, width=40, height=4, state=tk.DISABLED)
text_widget.pack(pady=10)

# Pokreni Tkinter glavni loop
root.mainloop()

