import socket

from src.config import FAMILY, HOST, PORT, TYPE


def create_socket_client():
    print("Creating client socket .....")
    res_list = socket.getaddrinfo(host=HOST, port=PORT, family=FAMILY, type=TYPE)
    _, _, _, _, sockaddr = res_list[0]
    s = socket.socket(family=FAMILY, type=TYPE)
    s.connect(sockaddr)

    print("Binded socket address .....")

    return s


def user_request(sock: socket.socket):
    user_message = input("User: ")
    client_socket.send(user_message.encode())


def create_user_name(sock: socket.socket):
    print("Please enter a user name")
    user_message = input("User: ")
    client_socket.send(user_message.encode())


if __name__ == "__main__":
    client_socket = create_socket_client()
    create_user_name(sock=socket)
    print("Please choose between three options: @name, @chatroom ")
    user_request(sock=client_socket)
