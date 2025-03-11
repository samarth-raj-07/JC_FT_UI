import socket
import tkinter as tk
from tkinter import messagebox

# Bridge PC IP and Port (Update with actual IP of Bridge PC)
BRIDGE_PC_IP = "192.168.0.107"  
BRIDGE_PC_PORT = 5000  

def request_file():
    filename = entry.get().strip()
    
    if not filename:
        messagebox.showerror("Error", "Please enter a filename")
        return
    
    try:
        # Connect to Bridge PC
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((BRIDGE_PC_IP, BRIDGE_PC_PORT))
        client.send(filename.encode())

        # Receive the file
        with open(filename, "wb") as file:
            while True:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)

        messagebox.showinfo("Success", f"File '{filename}' received successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get file: {e}")
    
    finally:
        client.close()

# GUI setup
root = tk.Tk()
root.title("File Transfer")
root.geometry("300x200")

tk.Label(root, text="Enter filename:").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

tk.Button(root, text="Request File", command=request_file).pack(pady=10)

root.mainloop()
