import socket
import os

# Server settings
HOST = "0.0.0.0"  # Accept connections from any IP
PORT = 12345
SAVE_DIR = "C:\\Received_Files"  # Change this to your desired folder

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def receive_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on port {PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")

            try:
                # Receive file metadata (name and size)
                metadata = conn.recv(1024).decode()
                file_name, file_size = metadata.split("|")
                file_size = int(file_size)

                save_path = os.path.join(SAVE_DIR, file_name)
                print(f"Receiving: {file_name} ({file_size} bytes) -> {save_path}")

                # Receive and save the file
                with open(save_path, "wb") as file:
                    received_bytes = 0
                    while received_bytes < file_size:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        file.write(chunk)
                        received_bytes += len(chunk)

                print(f"File saved to {save_path}")

            except Exception as e:
                print(f"Error receiving file: {e}")

            finally:
                conn.close()

if __name__ == "__main__":
    receive_file()
