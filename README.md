# 💬 Multi-Room Secure Chat System with File Transfer

## 📌 Project Overview

This project implements a scalable **client-server chat application** using low-level TCP sockets in Python. It supports multiple concurrent clients, enabling users to communicate in chat rooms, send private messages, and transfer files securely.

The system uses a custom **JSON-based communication protocol** and ensures **ordered message delivery** using synchronization mechanisms. Secure communication is achieved using **SSL/TLS encryption**.

---

## 🚀 Features

- 👥 Multi-client support using TCP sockets  
- 🏠 Multiple chat rooms  
- 💬 Real-time messaging within rooms  
- 🔒 Private messaging between users  
- 📁 File transfer using Base64 encoding  
- 🔐 Secure communication using SSL/TLS  
- ⚙️ Custom JSON-based protocol  
- 🧵 Multithreading for concurrency  
- 🔁 Ordered message delivery using locks  
- ❌ Graceful handling of client disconnections  

---

## 🧠 System Architecture

### 🔹 Server
- Handles incoming client connections  
- Manages users and chat rooms  
- Routes messages (room / private / file transfer)  
- Ensures thread-safe operations using locks  
- Secures communication using SSL  

### 🔹 Client
- Connects securely to server  
- Sends commands and messages  
- Receives messages and files  
- Supports multiple operations via CLI commands  

---

## ⚙️ Technologies Used

- **Language:** Python  
- **Communication:** TCP Sockets  
- **Security:** SSL/TLS  
- **Concurrency:** Threading  
- **Data Format:** JSON  
- **File Encoding:** Base64  

---

## 🔄 Working Principle

1. Server starts and listens for incoming connections  
2. Each client connection is handled in a separate thread  
3. Clients register with a username  
4. Clients join chat rooms  
5. Messages are sent using JSON format  
6. Server processes:
   - Room messages → broadcast to room users  
   - Private messages → sent to specific user  
   - Files → encoded and transferred  
7. Locks ensure ordered and thread-safe message delivery  
8. SSL/TLS ensures encrypted communication   

---

## 🔐 SSL Certificate Setup (IMPORTANT)

Before running the server, generate SSL certificates:

```bash
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/CN=localhost"


# 🖥️ How to Run

## 1. Start Server
```bash
python server.py
```

## 2. Start Client(s)

Open a new terminal (you can open multiple terminals for multiple users):
```bash
python client.py
```

## 3. Register Users

In each client terminal, register with a username:
```bash
/register <username>
```

**Example:**
```bash
/register John
```

## 4. Join a Chat Room
```bash
/join room1
```

> All users must join the same room to communicate.

## 5. Send Messages
```bash
/msg hello everyone
```

> Messages will be visible to all users in the same room.

## 6. Send Private Messages
```bash
/pm <username> <message>
```

**Example:**
```bash
/pm user2 hi
```

> Only the specified user will receive this message.

## 7. Send Files

Make sure the file exists in your project folder.
```bash
/file <username> <filename>
```

**Example:**
```bash
/file user2 test.txt
```

> The receiving user will get the file saved as: `received_test.txt`
