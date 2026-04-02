import socket
import threading
import ssl

HOST = '127.0.0.1'
PORT = 5555

clients = {}
rooms = {}
room_locks = {}

def broadcast(room, message, sender=None):
    if room not in rooms:
        return
    with room_locks[room]:
        for user in list(rooms[room]):
            if user != sender:
                send_to_user(user, message)

def remove_user(username):
    for room in rooms:
        if username in rooms[room]:
            rooms[room].remove(username)
            broadcast(room, f"{username} left {room}")

def start_server():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"🔐 Secure Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        try:
            secure_conn = context.wrap_socket(conn, server_side=True)
            threading.Thread(target=handle_client, args=(secure_conn, addr)).start()
        except ssl.SSLError:
            conn.close()

if __name__ == "__main__":
    start_server()
