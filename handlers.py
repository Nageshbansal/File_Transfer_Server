import os

def help():
    send_data = "OK$"
    send_data += "LIST: List all the files from the server. \n"
    send_data +="UPLOAD path: Upload a file to the server. \n"
    send_data +="DELETE filename: Delete a file from the server. \n"
    send_data +="LOGOUT: Disconnect from the server. \n"
    send_data +="HELP: List all the commands. \n"

    return send_data

def list_handler(SERVER_DATA_PATH):
    files = os.listdir(SERVER_DATA_PATH)
    send_data = "OK$"

    if len(files) == 0:
        send_data += "The server directory is empty"
    else:
        send_data += "\n".join(f for f in files)
    
    return send_data


def upload_handler(SERVER_DATA_PATH,name,text):
    filepath = os.path.join(SERVER_DATA_PATH, name)
    with open(filepath, "w") as f:
        f.write(text)

    send_data = "OK$File uploaded successfully."
    return send_data

def delete_handler(SERVER_DATA_PATH, data):
    files = os.listdir(SERVER_DATA_PATH)
    send_data = "OK$"
    filename = data[1]

    if len(files) == 0:
        send_data += "The server directory is empty"
    else:
        if filename in files:
            os.system(f"rm {SERVER_DATA_PATH}/{filename}")
            send_data += "File deleted successfully."
        else:
            send_data += "File not found."
    
    return send_data