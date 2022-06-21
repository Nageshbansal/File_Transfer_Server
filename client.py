import os
import socket 
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"


def main():
    """
    creates a client, connects to server and check the msg recieved from server
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("$")

        if cmd == "OK":
            print(f"{msg}")
        
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break
        
        data = input("> ").split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "DELETE":
            client.send(f"{cmd}${data[1]}".encode(FORMAT))

        elif cmd == "UPLOAD":
            path = data[1]

            with open(f"{path}", "r") as f:
                text = f.read()

            filename = path.split("/")[-1]
            send_data = f"{cmd}${filename}${text}"
            client.send(send_data.encode(FORMAT))

    print("DISCONNECTED FROM SERVER")
    client.close()


if __name__ == "__main__":
    main()