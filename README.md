# 💬 Multi-Room Secure Chat System with File Transfer

## 📌 Project Overview

This project implements a scalable **client-server chat application** using TCP sockets in Python. It supports multiple concurrent clients, allowing users to communicate in chat rooms, send private messages, and transfer files.

The system uses a custom JSON-based protocol for communication and ensures message ordering within each room using synchronization mechanisms.

---

## 🚀 Features

- 👥 Multi-client support using TCP sockets  
- 🏠 Multiple chat rooms  
- 💬 Real-time messaging within rooms  
- 🔒 Private messaging between users  
- 📁 File transfer using Base64 encoding  
- ⚙️ Custom JSON-based protocol  
- 🧵 Multithreading for concurrency  
- 🔁 Ordered message delivery using locks  
- ❌ Graceful handling of client disconnections  

---

## 🧠 System Architecture

- **Server**:
  - Handles client connections
  - Manages chat rooms and users
  - Routes messages between clients

- **Client**:
  - Connects to server
  - Sends commands and messages
  - Receives messages and files

---

## ⚙️ Technologies Used

- Language: Python  
- Communication: TCP Sockets  
- Concurrency: Threading  
- Data Format: JSON  
- File Encoding: Base64  

---

## 🔄 Working Principle

1. Server listens for incoming connections  
2. Each client is handled using a separate thread  
3. Clients register and join chat rooms  
4. Messages are sent using JSON format  
5. Server processes:
   - Room messages → broadcast to room users  
   - Private messages → sent to specific user  
   - Files → encoded and transferred  
6. Locks ensure ordered delivery of messages  

---

# 💬 Multi-Room Secure Chat System with File Transfer

## 📌 Project Overview

This project implements a scalable **client-server chat application** using TCP sockets in Python. It supports multiple concurrent clients, allowing users to communicate in chat rooms, send private messages, and transfer files.

The system uses a custom JSON-based protocol for communication and ensures message ordering within each room using synchronization mechanisms.

---

## 🚀 Features

- 👥 Multi-client support using TCP sockets  
- 🏠 Multiple chat rooms  
- 💬 Real-time messaging within rooms  
- 🔒 Private messaging between users  
- 📁 File transfer using Base64 encoding  
- ⚙️ Custom JSON-based protocol  
- 🧵 Multithreading for concurrency  
- 🔁 Ordered message delivery using locks  
- ❌ Graceful handling of client disconnections  

---

## 🧠 System Architecture

- **Server**:
  - Handles client connections
  - Manages chat rooms and users
  - Routes messages between clients

- **Client**:
  - Connects to server
  - Sends commands and messages
  - Receives messages and files

---

## ⚙️ Technologies Used

- Language: Python  
- Communication: TCP Sockets  
- Concurrency: Threading  
- Data Format: JSON  
- File Encoding: Base64  

---

## 🔄 Working Principle

1. Server listens for incoming connections  
2. Each client is handled using a separate thread  
3. Clients register and join chat rooms  
4. Messages are sent using JSON format  
5. Server processes:
   - Room messages → broadcast to room users  
   - Private messages → sent to specific user  
   - Files → encoded and transferred  
6. Locks ensure ordered delivery of messages  

---

## 🖥️ How to Run

### 1. Start Server
```bash
python server.py
2. Start Client(s)

Open a new terminal (you can open multiple terminals for multiple users):

python client.py
3. Register Users

In each client terminal, register with a username:

/register username

Example:

/register aditi
4. Join a Chat Room
/join room1

All users must join the same room to communicate.

5. Send Messages
/msg hello everyone

Messages will be visible to all users in the same room.

6. Send Private Messages
/pm username message

Example:

/pm user2 hi

Only the specified user will receive this message.

7. Send Files

Make sure the file exists in your project folder.

/file username filename

Example:

/file user2 test.txt

The receiving user will get the file saved as:

received_test.txt
