import socket
import threading
import json
HOST = '127.0.0.1'
PORT = 5555
clients = {}          # username -> socket
rooms = {}            # room -> [usernames]
room_locks = {}       # room -> lock
def handle_client(conn, addr):
    username = None
    current_room = None
    try:
        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            msg = json.loads(data)
            action = msg.get("action")
            # REGISTER
            if action == "register":
                username = msg["username"]
                clients[username] = conn
                conn.send(f"Welcome {username}".encode())
            # JOIN ROOM
            elif action == "join":
                room = msg["room"]
                current_room = room
                if room not in rooms:
                    rooms[room] = []
                    room_locks[room] = threading.Lock()
                if username not in rooms[room]:
                    rooms[room].append(username)
                    broadcast(room, f"{username} joined {room}", username)
            # ROOM MESSAGE
            elif action == "message":
                text = msg["text"]
                if current_room:
                    broadcast(current_room, f"{username}: {text}", username)
            # PRIVATE MESSAGE
            elif action == "private":
                to_user = msg["to"]
                text = msg["text"]
                send_to_user(to_user, f"[PRIVATE] {username}: {text}")
            # FILE TRANSFER
            elif action == "file":
                to_user = msg["to"]
                filename = msg["filename"]
                filedata = msg["data"]
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
            if username in clients:
                del clients[username]
            remove_user(username)
        conn.close()
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"🚀 Server running on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        print(f"Connected: {addr}")
        threading.Thread(target=handle_client, args=(conn, addr)).start()
start_server()