import socket
import sys
import threading
import time

import readchar


from src.config import FAMILY, HOST, PORT, TYPE

input_buffer = []


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


def print_to_cli(client_socket: socket.socket, user_name: str):
    while True:
        message = client_socket.recv(1024).decode()
        sys.stdout.write("\r\033[K")
        sys.stdout.write(f"{message}\n")
        sys.stdout.write(f"{user_name}: {''.join(input_buffer)}")
        sys.stdout.flush()
        input_buffer.clear()


if __name__ == "__main__":
    client_socket = create_socket_client()
    user_name = create_user_name(client_socket=client_socket)

    thread = threading.Thread(target=print_to_cli, args=(client_socket, user_name))
    thread.daemon = True
    thread.start()
    print("Please choose between three options: @name, @chatroom ")

    while True:
        sys.stdout.write(f"\n{user_name}: ")
        sys.stdout.flush()
        while True:
            key = readchar.readkey()

            if key in ("\x08", "\x7f"):
                if input_buffer:
                    input_buffer.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            elif key == "\r":
                break
            else:
                input_buffer.append(key)
                sys.stdout.write(key)
                sys.stdout.flush()

        client_socket.send("".join(input_buffer).encode())
        input_buffer.clear()
