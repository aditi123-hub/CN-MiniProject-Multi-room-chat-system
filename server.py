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

# ---------- Core ----------
def broadcast(room, msg, sender=None):
    if room not in rooms:
        return
    for user in rooms[room]:
        if user != sender and user in clients:
            send_msg(clients[user], msg)

def remove_user(username):
    with locks["rooms"]:
        for room in rooms:
            if username in rooms[room]:
                rooms[room].remove(username)

# ---------- Client Handler ----------
def handle_client(conn, addr):
    username = None
    current_room = None

    print(f"[CONNECTED] {addr}")

    try:
        while True:
            msg = recv_msg(conn)
            if not msg:
                break

            print("[RECEIVED]", msg)  # DEBUG

            msg_type = msg.get("type")

            if msg_type == "register":
                username = msg["username"]

                with locks["clients"]:
                    if username in clients:
                        send_msg(conn, {"type": "error", "msg": "Username taken"})
                        continue
                    clients[username] = conn

                send_msg(conn, {"type": "info", "msg": f"Welcome {username}"})

            elif msg_type == "join":
                room = msg["room"]
                current_room = room

                with locks["rooms"]:
                    rooms.setdefault(room, []).append(username)

                broadcast(room, {
                    "type": "info",
                    "msg": f"{username} joined {room}"
                }, username)

            elif msg_type == "message":
                if current_room:
                    broadcast(current_room, {
                        "type": "message",
                        "from": username,
                        "text": msg["text"]
                    }, username)

            elif msg_type == "private":
                to_user = msg["to"]
                if to_user in clients:
                    send_msg(clients[to_user], {
                        "type": "private",
                        "from": username,
                        "text": msg["text"]
                    })

            elif msg_type == "file":
                to_user = msg["to"]

                print(f"[FILE] {username} → {to_user}: {msg['filename']}")

                if to_user in clients:
                    send_msg(clients[to_user], {
                        "type": "file",
                        "from": username,
                        "filename": msg["filename"],
                        "data": msg["data"]
                    })
                else:
                    send_msg(conn, {
                        "type": "error",
                        "msg": "User not online"
                    })

    except Exception as e:
        print("[ERROR]", e)

    finally:
        if username:
            with locks["clients"]:
                clients.pop(username, None)
            remove_user(username)
        conn.close()
        print(f"[DISCONNECTED] {addr}")


def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("cert.pem", "key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"🔐 Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        try:
            secure_conn = context.wrap_socket(conn, server_side=True)
            threading.Thread(
                target=handle_client,
                args=(secure_conn, addr),
                daemon=True
            ).start()
        except ssl.SSLError:
            conn.close()

if __name__ == "__main__":
    start_server()
