import socket
import select
import time
from typing import Dict, Tuple

from src.config import FAMILY, HOST, PORT, TYPE

connections: Dict[Tuple[str, int], socket.socket] = {}
name_to_addr: Dict[str, Tuple[str, int]] = {}


def create_socket_server():

    print("Server connecting .....")

    res_list = socket.getaddrinfo(host=HOST, port=PORT, family=FAMILY, type=TYPE)
    _, _, _, _, sockaddr = res_list[0]
    server_socket = socket.socket(family=FAMILY, type=TYPE)
    server_socket.bind(sockaddr)

    server_socket.listen(2)

    connections[sockaddr] = server_socket

    print("Server created .....")
    print(f"Server address binded to {sockaddr} .....")

    return server_socket


def intialise_client(connection: socket.socket, client_addr):
    connections[client_addr] = connection
    user_name = connection.recv(1024).decode()
    name_to_addr[user_name] = client_addr
    print(f"Socket Created for {user_name}, {client_addr}")


def handle_client(connection: socket.socket):
    data = connection.recv(1024).decode()
    data_tokens = data.split()
    if data_tokens[0][0] != "@":
        connection.send("[ERROR] Missing @ ")
        return
    if data_tokens[0][1:] not in name_to_addr:
        connection.send("[ERROR] Target user not found")
        return

    reciever_name = data_tokens[0][1:]
    reciever_addr = name_to_addr[reciever_name]
    reciever_socket = connections[reciever_addr]
    reciever_msg = " ".join(data_tokens[1:])
    reciever_socket.send(reciever_msg.encode())


if __name__ == "__main__":
    server_socket = create_socket_server()

    while True:
        connections_arr = list(connections.values())

        readable, writable, _ = select.select(connections_arr, [], [])

        for sock in readable:
            if sock == server_socket:
                conn, client_addr = server_socket.accept()

                intialise_client(connection=conn, client_addr=client_addr)
            else:
                handle_client(
                    connection=sock,
                )

        print(readable)
