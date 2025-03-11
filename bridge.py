# BRIDGE
import socket

# Bridge PC settings
BRIDGE_HOST = ""  # Listen on all interfaces
BRIDGE_PORT = 5000  # Port for communication with Signal PC
SERVER_PC_IP = "192.168.0.110"  # Server PC IP
SERVER_PC_PORT = 6000  # Port on which Server PC is listening

def handle_client(conn):
    filename = conn.recv(1024).decode()
    print(f"Requested file: {filename}")

    # Request file from Server PC
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect((SERVER_PC_IP, SERVER_PC_PORT))
    server_conn.send(filename.encode())

    # Receive the file from Server PC
    with open(filename, "wb") as file:
        received_data=False
        while True:
            data = server_conn.recv(4096)
            if not data:
                break
            file.write(data)
            received_data=True
    server_conn.close()

    # Send file to Signal PC
    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            conn.send(chunk)

    print(f"File {filename} sent to Signal PC")
    conn.close()

# Start the Bridge PC server
bridge_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bridge_server.bind((BRIDGE_HOST, BRIDGE_PORT))
bridge_server.listen(5)
print("Bridge PC listening for connections...")

while True:
    client_conn, _ = bridge_server.accept()
    handle_client(client_conn)
