
# ---------- Message Framing ----------
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
