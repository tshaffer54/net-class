"""
GEO TCP Client
"""

# !/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

HOST = 'localhost'
PORT = 4300


def client():
    """Main client loop"""
    # TODO: Implement client-side tasks
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print('Connected to {}:{}'.format(HOST, PORT))
        name = input("Please enter a country name: ")
        s.sendall("{}".format(name).encode())


def main():
    """Main function"""
    client()


if __name__ == "__main__":
    main()
