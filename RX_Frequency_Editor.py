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
        self.root.title("RXFREQ Editor by 9A4AM")
        root.configure(background='black')

        text_var = tk.StringVar()
        text_var.set("File = start_rtlsdr.sh -> Freq in Hertz")
        label = tk.Label(root, textvariable=text_var,font=("Arial", 10, "bold"),bg="black", fg="yellow")
        label.pack(pady=10)
        self.textbox = tk.Entry(root, font = 'sans 16 bold', bg = 'light blue', justify='center')
        self.textbox.pack(pady=10)
        self.textbox.bind("<Button-1>", self.show_keyboard)

        self.save_button = tk.Button(root, text="SAVE", command=self.save_value, height = 1, width = 16, font = 'sans 16 bold', bg = 'green')
        self.save_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="EXIT", command=self.exit_app, height = 1, width = 16, font = 'sans 16 bold', bg = 'red')
        self.exit_button.pack(pady=10)

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
            messagebox.showerror("Error", "start_rtlsdr.sh file not found")

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
            # self.root.quit()  # Zatvori aplikaciju
            # self.exit_app()
        except FileNotFoundError:
            messagebox.showerror("Error", "start_rtlsdr.sh file not found")

    def show_keyboard(self, event):
        # Očisti textbox pri otvaranju tipkovnice
        self.textbox.delete(0, tk.END)

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
                self.save_value()  # Spremi vrijednost i zatvori aplikaciju
                keyboard_window.destroy()
            else:
                current_text = self.textbox.get()
                if len(current_text) < 9:
                    self.textbox.insert(tk.END, key)

        for i, button in enumerate(buttons):
            action = lambda x=button: key_press(x)
            b = tk.Button(keyboard_window, text=button, width=5, height=2, command=action)
            b.grid(row=i//3, column=i%3)

    def exit_app(self):
        # self.root.quit()
        root.destroy()
        # sys.exit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RxFreqEditor(root)
    root.mainloop()
