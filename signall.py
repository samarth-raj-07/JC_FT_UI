import socket
import tkinter as tk
from tkinter import messagebox

# Bridge PC IP and Port 
BRIDGE_PC_IP = "192.168.0.107"  
BRIDGE_PC_PORT = 5001

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

        # Receive first response to check if the file exists
        response = client.recv(4096)
        if response == b"FILE_NOT_FOUND":
            messagebox.showerror("Error", f"File '{filename}' not found on Server PC")
            return  # Exit function without writing file

        # Save received data into file
        with open(filename, "wb") as file:
            file.write(response)  # Write the first received chunk
            while True:
                data = client.recv(4096)
                if not data:
                    break
                file.write(data)

        messagebox.showinfo("Success", f"File '{filename}' received successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to get file: {e}")
    
    finally:
        client.close()  # Ensure socket is closed

# GUI setup
root = tk.Tk()
root.title("File Transfer")
root.geometry("300x200")

tk.Label(root, text="Enter filename:").pack(pady=10)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

tk.Button(root, text="Request File", command=request_file).pack(pady=10)

root.mainloop()
