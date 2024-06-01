#-------------------------------------------------------------------------------
# Name:        Horus decoder v2
# Purpose:
#
# Author:      9A4AM
#
# Created:     01.06.2024
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

    # Pokreni provjeru loga zasebno
    threading.Thread(target=update_log).start()
    start_button.config(state="disabled")
def update_log():
    # Provjeri log fajl periodički
    while True:
        try:
            with open('log_horus', 'r') as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]
                    call, tim, lat, lon, alt, batt = parse_log_line(last_line)
                    update_text(call, tim, lat, lon, alt, batt)
        except FileNotFoundError:
            pass

        time.sleep(3)  # Provjeravaj svakih 3 sekunde

def parse_log_line(last_line):
    # Parsiraj liniju loga i izvuci Call, time, Lat, Lon, Alt, Dir, Batt
    parts = last_line.strip().split(',')
    call = parts[0][3:]  # Makni prva tri karaktera
    tim = parts[2]
    lat = parts[3]
    lon = parts[4]
    alt = parts[5]
    batt = parts[9][:4]
    return call, tim, lat, lon, alt, batt

def update_text(call, tim, lat, lon, alt, batt):
    # Ažuriraj tekstualno polje sa novim vrijednostimea
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, f"Frequency: 437.600MHz\nID: {call}  Time: {tim}\nLat: {lat}  Lon: {lon}  Alt: {alt}\nBatt: {batt}V")
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
root.configure(background='black')
root.title("Horus Decoder by 9A4AM")
os.remove("log_horus")

# Kreiraj gumb za pokretanje skripte
start_button = tk.Button(root, text="Start decoder", command=run_horus_script)
start_button.pack(pady=10)

# Kreiraj gumb za zaustavljanje skripte
stop_button = tk.Button(root, text="Stop decoder & Exit", command=stop_horus_script)
stop_button.pack(pady=10)

# Kreiraj tekstualni widget sa skrolanjem za prikaz loga
text_widget = scrolledtext.ScrolledText(root, width=40, height=5, state=tk.DISABLED)
text_widget.pack(pady=10)

# Pokreni Tkinter glavni loop
root.mainloop()
