# 🧠 CLI Chat Room Server (Python)

This is a simple **command-line chat server** built with Python's `socket` and `select` libraries. It supports **multiple clients**, basic commands (like `@all` and `@people`), and tracks connected users with socket-to-name mappings.

---

## 📦 Features

- Accepts multiple clients using `select` (non-blocking I/O)
- Username registration on connect
- Private messaging using `@username`
- Broadcast messaging using `@all`
- Online user listing via `@people`
- Graceful disconnect handling
- Lightweight and dependency-free (except `readchar` on client)

---

## 🏁 Getting Started

### 1. Install Python
Ensure you're using Python 3.6+.

### 2. Configure Host Settings

Edit `src/config.py`:

```python
FAMILY = socket.AF_INET
TYPE = socket.SOCK_STREAM
HOST = "127.0.0.1"
PORT = 12345  # or any available port
```

---

## 🚀 Running the Server

```bash
python src/server/server.py
```

---

## 💬 Commands Supported

### `@people`
Lists all connected users **excluding you**.

### `@all <message>`
Broadcasts a message to **all** users.

### `@username <message>`
Sends a private message to a specific user.

### _(Client-side only)_ `@exit`
Closes the connection and exits the client.

---

## 🧱 Code Structure

### 🔹 Server

- `create_socket_server()`  
  Sets up and binds the main server socket.

- `intialise_client(connection, client_addr)`  
  Handles username registration.

- `handle_client(connection)`  
  Processes incoming messages and commands.

- `disconnect_client(sock)`  
  Cleans up tracking maps and closes the socket.

- `main loop`  
  Uses `select.select()` to multiplex sockets and handle activity.

---

## 🛡 Error Handling

- Catches and logs broken client connections
- Automatically removes disconnected clients from all tracking dictionaries

---

## 📦 Dependencies

- Python Standard Library:
  - `socket`
  - `select`
  - `time`
  - `typing`

Optional (client side only):
- `readchar` – for interactive typing in terminal

---

## 🛠️ Future Ideas

- Add `@room` support for chatrooms
- Logging chat history
- Client authentication
- WebSocket frontend

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🤝 Contributing

PRs welcome! File an issue
