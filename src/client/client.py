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


def create_user_name(client_socket: socket.socket):
    print("Please enter a user name")
    user_message = input("User: ")
    client_socket.send(user_message.encode())
    return user_message


if __name__ == "__main__":
    client_socket = create_socket_client()
    user_name = create_user_name(client_socket=client_socket)

    while True:
        print("Please choose between three options: @name, @chatroom ")

        user_message = input(f"{user_name}: ")
        client_socket.send(user_message.encode())

        print(client_socket.recv(1024).decode())
