import socket
import threading
import json
import base64
import os

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
def receive():
    while True:
        try:
            data = client.recv(4096)
            try:
                msg = json.loads(data.decode())
                if msg.get("action") == "file":
                    filename = "received_" + msg["filename"]
                    with open(filename, "wb") as f:
                        f.write(base64.b64decode(msg["data"]))
                    print(f"\n📁 File received from {msg['from']}: {filename}")
            except:
                print("\n" + data.decode())
        except:
            print("Disconnected from server")
            break
def send():
    while True:
        cmd = input()
        # REGISTER
        if cmd.startswith("/register"):
            username = cmd.split()[1]
            client.send(json.dumps({
                "action": "register",
                "username": username
            }).encode())
        # JOIN ROOM
        elif cmd.startswith("/join"):
            room = cmd.split()[1]
            client.send(json.dumps({
                "action": "join",
                "room": room
            }).encode())
        # MESSAGE
        elif cmd.startswith("/msg"):
            text = " ".join(cmd.split()[1:])
            client.send(json.dumps({
                "action": "message",
                "text": text
            }).encode())
        # PRIVATE MESSAGE
        elif cmd.startswith("/pm"):
            parts = cmd.split()
            to_user = parts[1]
            text = " ".join(parts[2:])
            client.send(json.dumps({
                "action": "private",
                "to": to_user,
                "text": text
            }).encode())
        # FILE TRANSFER
        elif cmd.startswith("/file"):
            parts = cmd.split()
            to_user = parts[1]
            filepath = parts[2]
            if not os.path.exists(filepath):
                print("❌ File not found!")
                continue
            with open(filepath, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            client.send(json.dumps({
                "action": "file",
                "to": to_user,
                "filename": os.path.basename(filepath),
                "data": data
            }).encode())
threading.Thread(target=receive).start()
send()