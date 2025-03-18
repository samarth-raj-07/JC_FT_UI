# MAIN UI
import shutil
import os
import tkinter as tk
from tkinter import filedialog, messagebox

#Server shared folder path
SERVER_PATH =r"\\107.100.74.74\Assembly Inspection Group\Ankit Sharma-1\Setup Files"

#Target PC groups
GROUP_1= ["192.68.10.111", "192.68.10.112", "192.68.10.113", "192.68.10.114"]
GROUP_2= ["192.68.10.115", "192.68.10.116", "192.68.10.117", "192.68.10.118"]
GROUP_3= ["192.68.10.119", "192.68.10.120", "192.68.10.121", "192.68.10.122"]

selected_folder = ""

def fetch_folder():
    global selected_folder
    folder_name = folder_entry.get().strip()
    if not folder_name:
        messagebox.showerror("Error", "Please enter a folder name.")
        return

    source_folder = os.path.join(SERVER_PATH, folder_name)
    if not os.path.exists(source_folder):
        messagebox.showerror("Error", "Folder not found on server.")
        return
    
    destination_path = filedialog.askdirectory(title="Select Save Location")
    if not destination_path:
        return # User canceled
    selected_folder = os.path.join(destination_path, folder_name)

    try:
        shutil.copytree(source_folder, selected_folder, dirs_exist_ok=True)
        messagebox.showinfo("Success", f"Folder '{folder_name}' copied successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy folder:'\n'{e}")

def set_group_ips(group):
    '''Set the IPs of the selected group into the input box.'''
    ip_input.delete(0, tk.END)
    ip_input.insert(0, " ".join(group))

def send_files():
    '''Send the fetched folder to selected IPs.'''
    if not selected_folder:
        messagebox.showerror("Error", "No folder fetched.Fetch a folder first.")
        return
    target_ips = ip_input.get().strip().split()
    if not target_ips:
        messagebox.showerror("Error", "Please select or enter target IPs.")
        return
    success_log=[]
    error_log = []

    for ip in target_ips:
        target_path = rf"\\{ip}\TargetFolder"

        try:
            shutil.copytree(selected_folder, target_path,dirs_exist_ok=True)
            success_log.append(f"Success: {ip}")

        except Exception as e:
            error_log.append(f"Failed: {ip} - {str(e)}")

    # Log results
    log_text = "\n".join(success_log + error_log)

    with open("transfer_log.txt", "w") as log_file:
        log_file.write(log_text)
    messagebox.showinfo("Transfer Complete", f"Check 'transfer_log.txt' for details.")

def show_log():
    """Display the log in a pop-up."""
    try:
        with open("transfer_log.txt", "r") as log_file:
            log_content = log_file.read()

        log_window = tk.Toplevel(root)
        log_window.title("Transfer Log")
        log_text = tk.Text(log_window, wrap="word")
        log_text.insert("1.0", log_content)
        log_text.pack(expand=True, fill="both")

    except FileNotFoundError:
        messagebox.showerror("Error", "No log file found.")

def add_placeholder(entry_widget, placeholder_text):
    """Adds a placeholder to an Entry widget with proper behavior."""
    
    def on_focus_in(event):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, "end")
            entry_widget.config(fg="black")

    def on_focus_out(event):
        if not entry_widget.get().strip():  # Ensures placeholder returns if input is cleared
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(fg="grey")

    # Initial placeholder setup
    entry_widget.insert(0, placeholder_text)
    entry_widget.config(fg="grey")

    # Bind events
    entry_widget.bind("<FocusIn>", on_focus_in)
    entry_widget.bind("<FocusOut>", on_focus_out)

# GUI setup

root = tk.Tk()
root.title("JC_FT_Main")
root.geometry("600x300")

tk.Label(root, text="JC_FT_Main", font=("Arial", 16, "bold")).pack(pady=10)

#Phase 1-Fetch Folder
tk.Label(root, text="Enter Folder Name:").pack(pady=5)
folder_entry = tk.Entry(root, width=40)
folder_entry.pack(pady=5)
add_placeholder(folder_entry, "Enter folder name")
tk.Button(root, text="Fetch", command=fetch_folder).pack(pady=10)

#Phase 2-Target Selection
frame = tk.Frame(root)
frame.pack(pady=10)
tk.Button(frame, text="12M", command=lambda:
set_group_ips(GROUP_1)).grid(row=0, column=0, padx=5)
tk.Button(frame, text="29M", command=lambda:set_group_ips(GROUP_2)).grid(row=0, column=1, padx=5)
tk.Button(frame, text="M606s", command=lambda: set_group_ips(GROUP_3)).grid(row=0, column=2, padx=5)
ip_input = tk.Entry(frame, width=40)
ip_input.grid(row=0, column=3, padx=5)
add_placeholder(ip_input, "Enter target IPs")

# Send & Log Buttons
tk.Button(root, text="Send",command=send_files).pack(pady=5)
tk.Button(root, text="Log",command=show_log).pack(pady=5)
root.mainloop()