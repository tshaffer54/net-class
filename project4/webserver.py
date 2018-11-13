"""Python Web server implementation"""
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
import sys

server = socket(AF_INET, SOCK_STREAM)

ADDRESS = "127.0.0.2"  # Local client is going to be 127.0.0.1
PORT = 4300  # Open http://127.0.0.2:4300 in a browser
LOGFILE = "webserver.log"


def main():
    """Main loop"""
    server.bind((ADDRESS, PORT))
    server.listen(1)
    print('server listening....')

    conn, addr = server.accept()
    print('got connection from', addr)
    time = datetime.now()
    data = conn.recv(1024)
    filename = 'alice30.txt'
    logr = open(LOGFILE, "r")
    log = open(LOGFILE, "w")
    # print(repr(data))
    # print(sys.argv.__len__())

    if sys.argv.__len__() >= 2:
        print('sys fail')
        if sys.argv.__contains__('POST'):
            return conn.send(bytes('405 Method Not Allowed', 'utf-8'))

        if not sys.argv.__contains__('/alice30.txt'):
            return conn.send(bytes('404 Not Found', 'utf-8'))

    logrl = []
    for line in logr:
        logrl.append(line)

    log.write(str(time) + " | ")
    log.write(filename + " | ")
    log.write(ADDRESS + " | ")
    log.write(str(data, 'utf-8'))

    f = open(filename, 'rb')
    length = 0
    for line in f:
        length += len(line)

    f.close()

    date = str(datetime.today())

    conn.send(bytes("HTTP/1.1 200 OK\n"
                    + "Content Length: " + str(length) + "\n"
                    + "Content Type: text/plain;\n"
                    + "charset=utf-8\n"
                    + "Date: " + date + "\n"
                    + "Last Modified: " + logr.readline() + "\n"
                    + "Server: CS430-Tristan", 'utf-8'))

    t = open(filename, 'rb')
    l = t.read(1024)
    while l:
        conn.send(l)
        l = t.read(1024)

    t.close()

    print('done sending')
    conn.close()


if __name__ == "__main__":
    main()
