import socket
import threading
import json
import ssl
import struct
import base64

HOST = '10.1.4.171'
PORT = 5555

# ---------- Framing ----------
def send_msg(conn, msg):
    data = json.dumps(msg).encode()
    length = struct.pack(">I", len(data))
    conn.sendall(length + data)

def recv_msg(conn):
    raw_len = conn.recv(4)
    if not raw_len:
        return None
    msg_len = struct.unpack(">I", raw_len)[0]
    data = b''
    while len(data) < msg_len:
        chunk = conn.recv(msg_len - len(data))
        if not chunk:
            return None
        data += chunk
    return json.loads(data.decode())

# ---------- Setup ----------
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_client = context.wrap_socket(client)

secure_client.connect((HOST, PORT))

username = input("Enter username: ")
send_msg(secure_client, {
    "type": "register",
    "username": username
})

# ---------- Receive ----------
def receive():
    while True:
        msg = recv_msg(secure_client)
        if not msg:
            print("[DISCONNECTED]")
            break

        if msg["type"] == "message":
            print(f"{msg['from']}: {msg['text']}")

        elif msg["type"] == "private":
            print(f"[PRIVATE] {msg['from']}: {msg['text']}")

        elif msg["type"] == "file":
            data = base64.b64decode(msg["data"])
            filename = "received_" + msg["filename"]

            with open(filename, "wb") as f:
                f.write(data)

            print(f"[FILE RECEIVED] {filename}")

        elif msg["type"] == "info":
            print(f"[INFO] {msg['msg']}")

        elif msg["type"] == "error":
            print(f"[ERROR] {msg['msg']}")

# ---------- Write ----------
def write():
    while True:
        try:
            cmd = input()

            if cmd.startswith("/join"):
                _, room = cmd.split()
                send_msg(secure_client, {"type": "join", "room": room})

            elif cmd.startswith("/msg"):
                send_msg(secure_client, {
                    "type": "message",
                    "text": cmd[5:]
                })

            elif cmd.startswith("/pm"):
                _, user, text = cmd.split(" ", 2)
                send_msg(secure_client, {
                    "type": "private",
                    "to": user,
                    "text": text
                })

            elif cmd.startswith("/file"):
                _, user, path = cmd.split()

                with open(path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()

                send_msg(secure_client, {
                    "type": "file",
                    "to": user,
                    "filename": path,
                    "data": encoded
                })

                print("[FILE SENT]")

        except:
            break

# ---------- Start ----------
recv_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

recv_thread.start()
write_thread.start()

recv_thread.join()
write_thread.join()
