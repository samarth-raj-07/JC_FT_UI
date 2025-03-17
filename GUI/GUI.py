import tkinter as tk
from tkinter import filedialog, Toplevel, messagebox
import socket
import os

# Global log storage
log_messages = []

def browse_file(entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def send_file(line_number, target_ip_entry, path_entry, log_label):
    target_ip = target_ip_entry.get().strip()
    file_path = path_entry.get().strip()

    if not target_ip or target_ip == "Target IP":
        log_label.config(text=f"Line {line_number}: Error - Target IP missing!", fg="red")
        return
    
    if not file_path or file_path == "Select File":
        log_label.config(text=f"Line {line_number}: Error - No file selected!", fg="red")
        return
    
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((target_ip, 12345))  # Port 12345
            client_socket.sendall(f"{file_name}|{file_size}".encode())  # Send metadata
            
            with open(file_path, "rb") as file:
                while chunk := file.read(4096):  # Read and send in chunks
                    client_socket.sendall(chunk)

        log_label.config(text=f"Line {line_number}: File sent successfully!", fg="green")
        log_messages.append(f"Line {line_number}: Sent {file_name} to {target_ip}")

    except Exception as e:
        log_label.config(text=f"Line {line_number}: Error - {str(e)}", fg="red")
        log_messages.append(f"Line {line_number}: Error - {str(e)}")

def show_log():
    log_window = Toplevel(root)
    log_window.title("Log Messages")

    log_text = tk.Text(log_window, wrap="word", height=15, width=60)
    log_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    log_text.config(state="normal")
    log_text.delete("1.0", tk.END)
    for message in log_messages:
        log_text.insert(tk.END, message + "\n")
    log_text.config(state="disabled")

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.config(fg="gray")
    entry.bind("<FocusIn>", lambda e: (entry.delete(0, tk.END), entry.config(fg="black")) if entry.get() == placeholder_text else None)
    entry.bind("<FocusOut>", lambda e: (entry.insert(0, placeholder_text), entry.config(fg="gray")) if not entry.get() else None)

def on_enter(event):
    event.widget.config(relief="sunken")  # Add a pressed effect on hover

def on_leave(event):
    event.widget.config(relief="raised")  # Revert to normal state

def create_hover_button(master, text, command, bg_color=None):
    btn = tk.Button(master, text=text, width=9, command=command, bg=bg_color, relief="raised")
    btn.bind("<Enter>", on_enter)  # Bind hover effect for all buttons
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
    add_placeholder(path_entry, "Select File")
    path_entry.grid(row=i+1, column=3, padx=10, pady=5, sticky="w")
    
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
    
    for text, ip in zip(["MCA L", "MCA Main", "MCA UL"], ["192.168.1.1", "192.168.1.2", "192.168.1.3"]):
        btn = create_hover_button(btn_frame, text, lambda e=target_ip_entry, ip=ip: (e.delete(0, tk.END), e.insert(0, ip)), bg_color="yellow")
        btn.pack(side="left", expand=True, fill="both")
    
    create_hover_button(root, "Browse", lambda e=path_entry: browse_file(e)).grid(row=i+1, column=4, padx=5, pady=5, sticky="w")
    
    log_label = tk.Label(root, text="No action yet", fg="gray", width=40, anchor="w")
    log_label.grid(row=i+1, column=6, padx=5, pady=5, sticky="w")
    log_labels[i+1] = log_label
    
    create_hover_button(root, "Send", lambda ln=i+1, ip=target_ip_entry, p=path_entry, lbl=log_label: send_file(ln, ip, p, lbl)).grid(row=i+1, column=5, padx=5, pady=5, sticky="w")

create_hover_button(root, "Show Log", command=show_log).grid(row=8, column=0, columnspan=12, pady=10)

root.resizable(False, False)
root.mainloop()