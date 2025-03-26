import socket

from src.config import FAMILY, HOST, PORT, TYPE


def create_socket_server():

    print("Server connecting .....")

    res_list = socket.getaddrinfo(host=HOST, port=PORT, family=FAMILY, type=TYPE)
    _, _, _, _, sockaddr = res_list[0]
    server_socket = socket.socket(family=FAMILY, type=TYPE)
    server_socket.bind(sockaddr)

    server_socket.listen(10)

    print("Server created .....")
    print(f"Server address binded to {sockaddr} .....")

    return server_socket


def process_request(server_socket: socket.socket):

    print("Requests processing .....")
    server_socket.accept()


if __name__ == "__main__":
    server_socket = create_socket_server()
