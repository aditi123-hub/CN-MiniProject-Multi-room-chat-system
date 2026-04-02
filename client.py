import socket
import threading
import json
import ssl
import base64

HOST = '127.0.0.1'
PORT = 5555

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client)

secure_client.connect((HOST, PORT))

username = input("Enter username: ")
secure_client.send(json.dumps({
    "action": "register",
    "username": username
}).encode())

def receive():
    while True:
        try:
            data = secure_client.recv(4096)
            if not data:
                break

            try:
                msg = json.loads(data.decode())

                if msg.get("action") == "file":
                    filename = "received_" + msg["filename"]
                    file_bytes = base64.b64decode(msg["data"])
                    with open(filename, "wb") as f:
                        f.write(file_bytes)
                    print(f"\nFile received from {msg['from']}: {filename}")
                else:
                    print(msg)

            except:
                print(data.decode())

        except:
            break

def write():
    while True:
        cmd = input()

        if cmd.startswith("/join"):
            _, room = cmd.split()
            secure_client.send(json.dumps({
                "action": "join",
                "room": room
            }).encode())

        elif cmd.startswith("/msg"):
            text = cmd[5:]
            secure_client.send(json.dumps({
                "action": "message",
                "text": text
            }).encode())

        elif cmd.startswith("/pm"):
            _, user, text = cmd.split(" ", 2)
            secure_client.send(json.dumps({
                "action": "private",
                "to": user,
                "text": text
            }).encode())

        elif cmd.startswith("/file"):
            _, user, path = cmd.split()
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()

            secure_client.send(json.dumps({
                "action": "file",
                "to": user,
                "filename": path,
                "data": encoded
            }).encode())

threading.Thread(target=receive).start()
threading.Thread(target=write).start()
