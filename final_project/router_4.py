# !/usr/bin/env python3
# encoding: UTF-8


import os
import random
import select
import socket
import struct
import sys
import time

HOST_ID = os.path.splitext(__file__)[0].split("_")[-1]
THIS_NODE = "127.0.0.{}".format(HOST_ID)
PORT = 4300
NEIGHBORS = set()
ROUTING_TABLE = {}
TIMEOUT = 5
MESSAGES = [
    "Cosmic Cuttlefish",
    "Bionic Beaver",
    "Xenial Xerus",
    "Trusty Tahr",
    "Precise Pangolin"
]


def read_file(filename: str) -> None:
    distance = []
    key = ""
    ID = False
    file = open(filename, 'r')
    for line in file:
        line = line.strip('\n')
        distance.append(line)
    for item in distance:
        if ID:
            if len(item) is 0:
                ID = False
            else:
                NEIGHBORS.add(item[:-2])
                ROUTING_TABLE[THIS_NODE].append({item[:-2]: item[-1]})
        else:
            if len(item) is 9:
                if item == THIS_NODE:
                    ROUTING_TABLE.setdefault(item, [])
                    key = item
                    ID = True


def format_update():
    """Format update message"""
    table = ROUTING_TABLE[THIS_NODE]
    msg = [0]
    bmsg = []
    for i in table:
        for key, value in i.items():
            keys = key.split(".")
            for item in keys:
                msg.append(int(item))
            msg.append(int(value))
    for item in msg:
        tmp = item.to_bytes(1, 'big')
        if len(bmsg) == 0:
            bmsg = bytearray(tmp)
        else:
            bmsg.extend(tmp)
    return bmsg

    # raise NotImplementedError


def parse_update(msg, neigh_addr):
    """Update routing table"""
    raise NotImplementedError


def send_update(node):
    """Send update"""
    msg = format_update()
    port = 4300 + int(node[-1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(msg, (node, port))


def format_hello(msg_txt, src_node, dst_node):
    """Format hello message"""
    raise NotImplementedError


def parse_hello(msg):
    """Send the message to an appropriate next hop"""
    raise NotImplementedError


def send_hello(msg_txt, src_node, dst_node):
    message = format_hello(msg_txt, src_node, dst_node)
    raise NotImplementedError


def print_status():
    """Print status"""
    print('Routing Table')
    for key in ROUTING_TABLE.keys():
        print('\n', key)
        for item in ROUTING_TABLE[key]:
            for add in item:
                print(add, item[add])
    # raise NotImplementedError


def main(args: list):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((THIS_NODE, PORT))
    read_file('network_1_config.txt')
    print_status()
    for item in NEIGHBORS:
        send_update(item)
    # for item in NEIGHBORS:
    #     sock.sendall(send_update(item))
    try:
        resp = sock.recvfrom(1024)
        print(resp)
    finally:
        sock.close()


if __name__ == "__main__":
    main(sys.argv)
