
import shutil
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class JCFileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JC_FT_Main")
        self.root.geometry("800x500")  # Increased window size
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Server shared folder path
        # self.SERVER_PATH = r"\\107.100.74.74\Assembly Inspection Group\Ankit Sharma-1\Setup Files"
        self.SERVER_PATH = r"C:\\Users\\samar\\OneDrive\\Documents\\RESUME\\My resume"

        # Target PC groups
        self.GROUP_1 = ["192.68.10.111", "192.68.10.112", "192.68.10.113", "192.68.10.114"]
        self.GROUP_2 = ["192.68.10.115", "192.68.10.116", "192.68.10.117", "192.68.10.118"]
        self.GROUP_3 = ["192.68.10.119", "192.68.10.120", "192.68.10.121", "192.68.10.122"]

        self.selected_folder = ""  # Stores the fetched folder path

        # GUI Setup
        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components."""
        # Header
        header_frame = tk.Frame(self.root, bg="#4CAF50")  # Green background
        header_frame.pack(fill="x", pady=(0, 10))
        tk.Label(header_frame, text="JC_FT_Main", font=("Arial", 20, "bold"), bg="#4CAF50", fg="white").pack(pady=10)

        # Phase 1: Fetch Folder
        fetch_frame = tk.Frame(self.root, bg="#f0f0f0")
        fetch_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(fetch_frame, text="Enter Folder Name:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")
        self.folder_entry = ttk.Entry(fetch_frame, width=60, font=("Arial", 12))  # Wider entry field
        self.folder_entry.pack(pady=5, fill="x")
        self.add_placeholder(self.folder_entry, "Enter folder name")
        ttk.Button(fetch_frame, text="Fetch", command=self.fetch_folder, style="Accent.TButton").pack(pady=10)

        # Phase 2: Target Selection
        target_frame = tk.Frame(self.root, bg="#f0f0f0")
        target_frame.pack(pady=10, padx=20, fill="x")
        tk.Label(target_frame, text="Select Target Group:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w")

        button_frame = tk.Frame(target_frame, bg="#f0f0f0")
        button_frame.pack(pady=5, fill="x")
        ttk.Button(button_frame, text="12M", command=lambda: self.set_group_ips(self.GROUP_1), style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="29M", command=lambda: self.set_group_ips(self.GROUP_2), style="TButton").grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="M606s", command=lambda: self.set_group_ips(self.GROUP_3), style="TButton").grid(row=0, column=2, padx=5)

        self.ip_input = ttk.Entry(button_frame, width=60, font=("Arial", 12))  # Wider entry field
        self.ip_input.grid(row=0, column=3, padx=5)
        self.add_placeholder(self.ip_input, "Enter target IPs")

        # Send & Log Buttons
        action_frame = tk.Frame(self.root, bg="#f0f0f0")
        action_frame.pack(pady=20, padx=20, fill="x")
        ttk.Button(action_frame, text="Send", command=self.send_files, style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(action_frame, text="Log", command=self.show_log, style="TButton").pack(side="left", padx=5)

        # Configure ttk styles
        self.configure_styles()

    def configure_styles(self):
        """Configure ttk styles for a modern look with hover and click effects."""
        style = ttk.Style()
        style.theme_use("clam")  # Use the 'clam' theme for a modern look

        # Configure regular button style
        style.configure("TButton",
                        font=("Arial", 12),
                        padding=5,
                        background="#4CAF50",  # Green background
                        foreground="white",   # White text
                        borderwidth=2,         # Add border
                        relief="raised")       # Default raised appearance
        style.map("TButton",
                  background=[("active", "#45a049"), ("pressed", "#808080")],  # Darker green on hover, grey on press
                  foreground=[("pressed", "white"), ("!pressed", "white")],    # Keep text white
                  relief=[("pressed", "sunken"), ("!pressed", "raised")],       # Pressing effect
                  bordercolor=[("pressed", "#606060")])                         # Darker border on press

        # Configure  accent button style
        style.configure("Accent.TButton",
                        font=("Arial", 12, "bold"),
                        padding=5,
                        background="#2196F3",  # Blue background
                        foreground="white",     # White text
                        borderwidth=2,          # Add border
                        relief="raised")        # Default raised appearance
        style.map("Accent.TButton",
                  background=[("active", "#1e88e5"), ("pressed", "#808080")],  # Darker blue on hover, grey on press
                  foreground=[("pressed", "white"), ("!pressed", "white")],    # Keep text white
                  relief=[("pressed", "sunken"), ("!pressed", "raised")],      # Pressing effect
                  bordercolor=[("pressed", "#606060")])                         # Darker border on press

    def fetch_folder(self):
        """Fetch the folder from the server and copy it to a local destination."""
        folder_name = self.folder_entry.get().strip()
        if not folder_name:
            messagebox.showerror("Error", "Please enter a folder name.")
            return

        source_folder = os.path.join(self.SERVER_PATH, folder_name)
        if not os.path.exists(source_folder):
            messagebox.showerror("Error", f"Folder '{folder_name}' not found on server.")
            return

        destination_path = filedialog.askdirectory(title="Select Save Location")
        if not destination_path:
            return  # User canceled

        self.selected_folder = os.path.join(destination_path, folder_name)

        try:
            shutil.copytree(source_folder, self.selected_folder, dirs_exist_ok=True)
            messagebox.showinfo("Success", f"Folder '{folder_name}' copied successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy folder:\n{str(e)}")

    def set_group_ips(self, group):
        """Set the IPs of the selected group into the input box."""
        self.ip_input.delete(0, tk.END)
        self.ip_input.insert(0, " ".join(group))

    def send_files(self):
        """Send the fetched folder to the selected IPs."""
        if not self.selected_folder:
            messagebox.showerror("Error", "No folder fetched. Fetch a folder first.")
            return

        target_ips = self.ip_input.get().strip().split()
        if not target_ips:
            messagebox.showerror("Error", "Please select or enter target IPs.")
            return

        success_log = []
        error_log = []

        for ip in target_ips:
            target_path = rf"\\{ip}\TargetFolder"  # Ensure the target folder exists and is accessible
            try:
                shutil.copytree(self.selected_folder, target_path, dirs_exist_ok=True)
                success_log.append(f"Success: {ip}")
            except Exception as e:
                error_log.append(f"Failed: {ip} - {str(e)}")

        # Log results
        log_text = "\n".join(success_log + error_log)
        with open("transfer_log.txt", "a") as log_file:  # Append to log file
            log_file.write(f"Transfer Log:\n{log_text}\n\n")

        messagebox.showinfo("Transfer Complete", f"Check 'transfer_log.txt' for details.")

    def show_log(self):
        """Display the log in a pop-up."""
        try:
            with open("transfer_log.txt", "r") as log_file:
                log_content = log_file.read()

            log_window = tk.Toplevel(self.root)
            log_window.title("Transfer Log")
            log_window.geometry("600x400")  # Larger log window
            log_text = tk.Text(log_window, wrap="word", font=("Arial", 12))
            log_text.insert("1.0", log_content)
            log_text.pack(expand=True, fill="both", padx=10, pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "No log file found.")

    def add_placeholder(self, entry_widget, placeholder_text):
        """Adds a placeholder to an Entry widget with proper behavior."""
        def on_focus_in(event):
            if entry_widget.get() == placeholder_text:
                entry_widget.delete(0, "end")
                entry_widget.config(foreground="black")

        def on_focus_out(event):
            if not entry_widget.get().strip():
                entry_widget.insert(0, placeholder_text)
                entry_widget.config(foreground="grey")

        # Initial placeholder setup
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(foreground="grey")

        # Bind events
        entry_widget.bind("<FocusIn>", on_focus_in)
        entry_widget.bind("<FocusOut>", on_focus_out)


if __name__ == "__main__":
    root = tk.Tk()
    app = JCFileTransferApp(root)
    root.mainloop()

