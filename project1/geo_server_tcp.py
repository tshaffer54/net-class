"""
GEO TCP Server
"""
#!/usr/bin/env python3

from socket import socket, AF_INET, SOCK_STREAM

FILE_NAME = 'geo_world.txt'
HOST = 'localhost'
PORT = 4300


def read_file(filename: str) -> dict:
    """Read world territories and their capitals from the provided file"""
    world = dict()
    file = open(FILE_NAME, "r")
    for line in file:
        line = line.split()
        world.update({line[0]:line[2]})
    return world


def server(world: dict) -> None:
    """Main server loop"""
    # TODO: Implement server-side tasks
    with socket(AF_INET, SOCK_STREAM) as s:
        s. bind((HOST, PORT))
        s.listen(1)
        print("Listening on port {}".format(PORT))
        conn, addr = s.accept()
        with conn:
            print("Accepted connection from {}".format(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    print("Connection closed")
                    break
                name = data.decode()
                print("{}".format(name))
                cap = world[name]
                print(cap)
                print("{} is the captial of {}".format(cap, name))



def main():
    """Main function"""
    world = read_file(FILE_NAME)
    server(world)


if __name__ == "__main__":
    main()
