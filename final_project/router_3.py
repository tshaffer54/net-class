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
    table = ROUTING_TABLE
    change = False
    if neigh_addr[0] not in table.keys():
        table.setdefault(neigh_addr[0], [])
    length = len(msg)
    place = 1
    ip = ""
    while place != length:
        if place % 5 != 0:
            ip += str(msg[place]) + "."
            place += 1
        else:
            if {ip[:-1]: msg[place]} in table[neigh_addr[0]]:
                pass
            else:
                table[neigh_addr[0]].append({ip[:-1]: msg[place]})
                ip = ""
                place += 1
                change = True
    return change


def send_update(node):
    """Send update"""
    msg = format_update()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((THIS_NODE, PORT))
    s.sendto(msg, (node, (PORT + int(node[-1]))))


def format_hello(msg_txt, src_node, dst_node):
    """Format hello message"""
    msg = [1]
    bmsg = []
    src = src_node.split('.')
    dst = dst_node.split('.')
    for item in src:
        msg.append(int(item))
    for item in dst:
        msg.append(int(item))
    for item in msg:
        tmp = item.to_bytes(1, 'big')
        if len(bmsg) is 0:
            bmsg = bytearray(tmp)
        else:
            bmsg.extend(tmp)
    for i in range(len(msg_txt)):
        bmsg.extend(msg_txt[i].encode())
    return bmsg


def parse_hello(msg):
    """Send the message to an appropriate next hop"""
    typ = msg[0]
    src = msg[1:5]
    dst = msg[5:9]
    message = msg[9:]
    src_ip = ""
    dst_ip = ""
    for i in range(4):
        src_ip += str(src[i]) + "."
    src_ip = src_ip[:-1]
    for i in range(4):
        dst_ip += str(dst[i]) + "."
    dst_ip = dst_ip[:-1]
    message = message.decode()
    if typ is 1:
        return src_ip, dst_ip, message
    else:
        raise ValueError("Not a hello")


def send_hello(msg_txt, src_node, dst_node):
    message = format_hello(msg_txt, src_node, dst_node)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((THIS_NODE, PORT))
    s.sendto(message, (dst_node, (PORT + int(dst_node[-1]))))


def print_status():
    """Print status"""
    print('\n {} Routing Table'.format(THIS_NODE))
    for key in ROUTING_TABLE.keys():
        print('\n', key)
        for item in ROUTING_TABLE[key]:
            for add in item:
                print(add, item[add])


def main(args: list):
    read_file(args[1])
    # read_file('network_1_config.txt')
    print_status()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((THIS_NODE, PORT + int(HOST_ID)))
    for item in NEIGHBORS:
        send_hello(MESSAGES[random.randint(0, 4)], THIS_NODE, item)
    while True:
        data, addr = s.recvfrom(1024)
        if data[0] == 0:
            if parse_update(data, addr):
                print_status()
                for item in NEIGHBORS:
                    send_update(item)
        else:
            src, dest, mes = parse_hello(data)
            print('Source:', src, 'says', mes)


if __name__ == "__main__":
    main(sys.argv)
