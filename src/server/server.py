import socket
import select
from typing import Dict, Tuple

from src.config import FAMILY, HOST, PORT, TYPE

connections: Dict[Tuple[str, int], socket.socket] = {}
name_to_addr: Dict[str, Tuple[str, int]] = {}
socket_to_name: Dict[socket.socket, str] = {}


def create_socket_server():

    print("Server connecting .....")

    res_list = socket.getaddrinfo(host=HOST, port=PORT, family=FAMILY, type=TYPE)
    _, _, _, _, sockaddr = res_list[0]
    server_socket = socket.socket(family=FAMILY, type=TYPE)
    server_socket.bind(sockaddr)

    server_socket.listen()

    connections[sockaddr] = server_socket

    print("Server created .....")
    print(f"Server address binded to {sockaddr} .....")

    return server_socket


def intialise_client(connection: socket.socket, client_addr):
    user_name = connection.recv(1024).decode()
    connections[client_addr] = connection
    name_to_addr[user_name] = client_addr
    socket_to_name[connection] = user_name
    print(f"Socket Created for {user_name}, {client_addr}")


def handle_client(connection: socket.socket):
    data = connection.recv(1024).decode()
    data_tokens = data.split()

    if not data_tokens:
        return  # handle empty message

    if data_tokens[0][0] != "@":
        connection.send(b"[ERROR] Missing @ ")
        return

    if data_tokens[0] == "@people":
        people = [name for sock, name in socket_to_name.items() if sock != connection]
        response = (
            "Online: " + ",".join(people) if people else "No other users connected"
        )
        connection.send(response.encode())
        return

    if data_tokens[0] == "@all":
        sender_name = socket_to_name.get(connection, "Unknown")
        message_body = " ".join(data_tokens[1:])
        broadcast_msg = f"{sender_name}: {message_body}"

        for sock, name in socket_to_name.items():
            if sock != connection:  # Don't send back to the sender
                try:
                    sock.send(broadcast_msg.encode())
                except Exception as e:
                    print(f"Failed to send to {name}: {e}")
        return

    target_name = data_tokens[0][1:]
    if target_name not in name_to_addr:
        connection.send(b"[ERROR] Target user not found")
        return

    sender_name = socket_to_name.get(connection, "Unknown")  # 👈 Get sender name
    message_body = " ".join(data_tokens[1:])
    reciever_msg = f"{sender_name}: {message_body}"  # 👈 Include sender name

    reciever_addr = name_to_addr[target_name]
    reciever_socket = connections[reciever_addr]

    print("reciever_msg:", reciever_msg)
    reciever_socket.send(reciever_msg.encode())


def disconnect_client(sock: socket.socket):
    user_name = socket_to_name.get(sock, "<unknown>")
    print(f"Disconnecting client: {user_name}")

    # Remove from socket_to_name
    socket_to_name.pop(sock, None)

    # Remove from name_to_addr
    for name, addr in list(name_to_addr.items()):
        if connections.get(addr) == sock:
            name_to_addr.pop(name, None)
            break

    # Remove from connections
    for addr, s in list(connections.items()):
        if s == sock:
            connections.pop(addr, None)
            break

    try:
        sock.close()
    except Exception as e:
        print(f"[ERROR] Closing socket failed: {e}")


if __name__ == "__main__":
    server_socket = create_socket_server()

    while True:
        connections_arr = list(connections.values())

        readable, writable, _ = select.select(connections_arr, [], [])
        try:

            for sock in readable:
                if sock == server_socket:
                    conn, client_addr = server_socket.accept()

                    intialise_client(connection=conn, client_addr=client_addr)
                else:
                    handle_client(
                        connection=sock,
                    )

        except Exception as e:
            print(f"[SERVER LOOP ERROR] {e}")
            if sock != server_socket:
                disconnect_client(sock)
