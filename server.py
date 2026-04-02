import json

def send_to_user(user, message):
    if user in clients:
        try:
            clients[user].send(message.encode())
        except:
            pass

def handle_client(conn, addr):
    username = None
    current_room = None

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            try:
                msg = json.loads(data.decode())
            except:
                conn.send("Invalid JSON".encode())
                continue

            action = msg.get("action")

            if action == "register":
                username = msg.get("username")
                clients[username] = conn
                conn.send(f"Welcome {username}".encode())

            elif action == "join":
                room = msg.get("room")
                current_room = room

                if room not in rooms:
                    rooms[room] = []
                    room_locks[room] = threading.Lock()

                if username not in rooms[room]:
                    rooms[room].append(username)
                    broadcast(room, f"{username} joined {room}", username)

            elif action == "message":
                text = msg.get("text")
                if current_room:
                    broadcast(current_room, f"{username}: {text}", username)

            elif action == "private":
                to_user = msg.get("to")
                text = msg.get("text")
                if to_user in clients:
                    send_to_user(to_user, f"[PRIVATE] {username}: {text}")
                else:
                    send_to_user(username, "User not online")

            elif action == "file":
                to_user = msg.get("to")
                filename = msg.get("filename")
                filedata = msg.get("data")

                if to_user in clients:
                    clients[to_user].send(json.dumps({
                        "action": "file",
                        "filename": filename,
                        "data": filedata,
                        "from": username
                    }).encode())

    except Exception as e:
        print("Error:", e)

    finally:
        if username:
            clients.pop(username, None)
            remove_user(username)
        conn.close()
