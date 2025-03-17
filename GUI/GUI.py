import tkinter as tk
from tkinter import filedialog, Toplevel
import os

# Global log storage
log_messages = []

def browse_directory(entry):
    directory = filedialog.askdirectory()
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def send_file(line_number, target_ip_entry, path_entry, log_label):
    target_ip = target_ip_entry.get()
    directory = path_entry.get()
    message = (f"Line {line_number}: Sending files from {directory} to {target_ip}" 
               if target_ip and directory and target_ip != "Target IP" and directory != "Save Address" 
               else f"Line {line_number}: Error - Target IP or Directory missing!")
    
    log_messages.append(message)  # Store log
    log_label.config(text=message, fg="green" if "Sending" in message else "red")

def show_log():
    log_window = Toplevel(root)
    log_window.title("Log Messages")

    log_text = tk.Text(log_window, wrap="word", height=15, width=60)
    log_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    log_text.config(state="normal")  # Enable text insertion
    log_text.delete("1.0", tk.END)  # Clear previous content if any
    for message in log_messages:
        log_text.insert(tk.END, message + "\n")
    log_text.config(state="disabled")  # Disable editing after insertion

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg="gray")
    entry.bind("<FocusIn>", lambda e: (entry.delete(0, tk.END), entry.config(fg="black")) if entry.get() == placeholder_text else None)
    entry.bind("<FocusOut>", lambda e: (entry.insert(0, placeholder_text), entry.config(fg="gray")) if not entry.get() else None)

def on_enter(event):
    if event.widget["bg"] in ["yellow", "gold"]:  # If the button was yellow, change to gold on hover
        event.widget.config(bg="gold", fg="black")
    else:
        event.widget.config(bg="lightblue", fg="black")

def on_leave(event):
    if event.widget["bg"] == "gold":  # If it was gold (hovered), change it back to yellow
        event.widget.config(bg="yellow", fg="black")
    else:
        event.widget.config(bg="SystemButtonFace", fg="black")


def create_button_eqp(master, text, command):
    btn = tk.Button(master, text=text, width=9, command=command, bg="yellow")
    btn.original_bg = "yellow"  # Store the original color
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def create_button(master, text, command):
    btn = tk.Button(master, text=text, width=9, command=command)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

root = tk.Tk()
root.title("File Transfer GUI")

title_label = tk.Label(root, text="Samsung Display Noida", font=("Arial", 14, "bold"))
title_label.grid(row=0, column=0, columnspan=10, pady=10)

log_labels = {}
for i in range(7):
    tk.Label(root, text=f"Line {i+1}", font=("Arial", 12)).grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
    
    target_ip_entry = tk.Entry(root, width=15)
    add_placeholder(target_ip_entry, "Target IP")
    target_ip_entry.grid(row=i+1, column=2, padx=10, pady=5, sticky="w")
    
    path_entry = tk.Entry(root, width=30)
    add_placeholder(path_entry, "Save Address")
    path_entry.grid(row=i+1, column=3, padx=10, pady=5, sticky="w")
    
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
    
    for text, ip in zip(["MCA L", "MCA Main", "MCA UL"], ["192.168.1.1", "192.168.1.2", "192.168.1.3"]):
        create_button_eqp(btn_frame, text, lambda e=target_ip_entry, ip=ip: (e.delete(0, tk.END), e.insert(0, ip))).pack(side="left", expand=True, fill="both")
    
    create_button(root, "Browse", lambda e=path_entry: browse_directory(e)).grid(row=i+1, column=4, padx=5, pady=5, sticky="w")
    
    log_label = tk.Label(root, text="No action yet", fg="gray", width=40, anchor="w")
    log_label.grid(row=i+1, column=6, padx=5, pady=5, sticky="w")
    log_labels[i+1] = log_label
    
    create_button(root, "Send", lambda ln=i+1, ip=target_ip_entry, p=path_entry, lbl=log_label: send_file(ln, ip, p, lbl)).grid(row=i+1, column=5, padx=5, pady=5, sticky="w")

# tk.Button(root, text="Show Log", command=show_log).grid(row=8, column=0, columnspan=12, pady=10)
create_button(root, "Show Log", command=show_log).grid(row=8, column=0, columnspan=12, pady=10)

root.resizable(False, False)
root.mainloop()
