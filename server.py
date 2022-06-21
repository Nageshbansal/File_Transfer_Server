import os
import socket 
import sys
import threading
from handlers import delete_handler, help, list_handler, upload_handler 

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'server_data')


def handle_client(conn, addr):
    """
    sends a msg in the CMD$MSG format
    """
    print(f"[New Connection]: {addr} connected")
    conn.send("OK$Welcome to the File Server.".encode(FORMAT))

    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("$")
        cmd = data[0]

        if cmd == "HELP":
            response = help()
            conn.send(response.encode(FORMAT))

        elif cmd == "LIST":
            response = list_handler(SERVER_DATA_PATH)
            conn.send(response.encode(FORMAT))

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            response = upload_handler(SERVER_DATA_PATH, name, text)
            conn.send(response.encode(FORMAT))
            

        elif cmd == "DELETE":
            response = delete_handler(SERVER_DATA_PATH, data)
            conn.send(response.encode(FORMAT))

        elif cmd == "LOGOUT":
            break

def main():
    """
    starts the server and checks for new client connection requests
    """
    print("[STARTING]")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTNENING]")

    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except OSError:
            print("Server was killed")
        except KeyboardInterrupt:
            print('Server was killed')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == "__main__":
    main()