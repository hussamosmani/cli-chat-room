import socket

from src.config import FAMILY, HOST, PORT, TYPE

connections = {}
name_to_addr = {}


def create_socket_server():

    print("Server connecting .....")

    res_list = socket.getaddrinfo(host=HOST, port=PORT, family=FAMILY, type=TYPE)
    _, _, _, _, sockaddr = res_list[0]
    server_socket = socket.socket(family=FAMILY, type=TYPE)
    server_socket.bind(sockaddr)

    server_socket.listen(2)

    print("Server created .....")
    print(f"Server address binded to {sockaddr} .....")

    return server_socket


def intialise_client(connection: socket.socket, client_addr):
    connections[client_addr] = connection
    print("Socket established")
    user_name = connection.recv(1024)
    name_to_addr[user_name] = client_addr


def handle_client(connection: socket.socket, client_addr):
    print("Request accepted from ", client_addr)
    if client_addr not in connections:
        intialise_client(connection=connection, client_addr=client_addr)


if __name__ == "__main__":
    server_socket = create_socket_server()

    while True:
        print("Accepting requests .....")
        conn, client_addr = server_socket.accept()

        print(f"Accepted connection from {client_addr}")
        handle_client(connection=conn, client_addr=client_addr)
