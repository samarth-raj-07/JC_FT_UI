import socket
import os

# Server PC settings
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 6000  # Port for communication with Bridge PC
FILE_DIRECTORY = "/files"  # Update with the actual directory path

def handle_client(conn):
    filename = conn.recv(1024).decode()
    file_path = os.path.join(FILE_DIRECTORY, filename)

    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                conn.send(chunk)
        print(f"Sent file {filename} to Bridge PC")
    else:
        print(f"File {filename} not found")
    
    conn.close()

# Start the Server PC listener
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print("Server PC waiting for file requests...")

while True:
    client_conn, _ = server.accept()
    handle_client(client_conn)
