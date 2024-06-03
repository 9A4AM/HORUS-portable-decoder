#-------------------------------------------------------------------------------
# Name:        RxFrequencyEditor
# Purpose:
#
# Author:      9A4AM
#
# Created:     03.06.2024
# Copyright:   (c) 9A4AM@2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import messagebox

class RxFreqEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("RXFREQ Editor")

        self.textbox = tk.Entry(root, font=("Helvetica", 16), justify='center')
        self.textbox.pack(pady=20)
        self.textbox.bind("<Button-1>", self.show_keyboard)

        self.save_button = tk.Button(root, text="Save", command=self.save_value, font=("Helvetica", 16))
        self.save_button.pack(pady=20)

        self.load_value()

    def load_value(self):
        try:
            with open("start_rtlsdr.sh", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "RXFREQ=" in line:
                        start_index = line.find("RXFREQ=") + len("RXFREQ=")
                        self.current_value = line[start_index:start_index + 9]
                        self.textbox.insert(0, self.current_value)
                        break
        except FileNotFoundError:
            messagebox.showerror("Error", "start.sh file not found")

    def save_value(self):
        new_value = self.textbox.get()
        if len(new_value) != 9 or not new_value.isdigit():
            messagebox.showerror("Error", "RXFREQ must be a 9 digit number")
            return

        try:
            with open("start_rtlsdr.sh", "r") as file:
                lines = file.readlines()

            with open("start_rtlsdr.sh", "w") as file:
                for line in lines:
                    if "RXFREQ=" in line:
                        start_index = line.find("RXFREQ=") + len("RXFREQ=")
                        line = line[:start_index] + new_value + line[start_index + 9:]
                    file.write(line)
            messagebox.showinfo("Success", "Value saved successfully")
        except FileNotFoundError:
            messagebox.showerror("Error", "start.sh file not found")

    def show_keyboard(self, event):
        keyboard_window = tk.Toplevel(self.root)
        keyboard_window.title("Keyboard")

        # Postavljanje pozicije tipkovnice ispod glavnog prozora
        # x = self.root.winfo_x()
        # y = self.root.winfo_y() + self.root.winfo_height()
        # keyboard_window.geometry(f"+{x}+{y}")

        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'Clear', '0', 'Enter'
        ]

        def key_press(key):
            if key == "Clear":
                self.textbox.delete(0, tk.END)
            elif key == "Enter":
                keyboard_window.destroy()
            else:
                current_text = self.textbox.get()
                if len(current_text) < 9:
                    self.textbox.insert(tk.END, key)

        for i, button in enumerate(buttons):
            action = lambda x=button: key_press(x)
            b = tk.Button(keyboard_window, text=button, width=5, height=2, command=action)
            b.grid(row=i//3, column=i%3)

if __name__ == "__main__":
    root = tk.Tk()
    app = RxFreqEditor(root)
    root.mainloop()
