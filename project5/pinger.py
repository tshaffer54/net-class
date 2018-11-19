"""Python Pinger"""
# !/usr/bin/env python3
# encoding: UTF-8

import binascii
import os
import select
import struct
import sys
import time
import socket
import statistics

ECHO_REQUEST_TYPE = 8
ECHO_REPLY_TYPE = 0
ECHO_REQUEST_CODE = 0
ECHO_REPLY_CODE = 0
REGISTRARS = ["afrinic.net", "apnic.net", "arin.net", "lacnic.net", "ripe.net"]
# REGISTRARS = ["example.com"]


def print_raw_bytes(pkt: bytes) -> None:
    """Printing the packet bytes"""
    for i in range(len(pkt)):
        sys.stdout.write("{:02x} ".format(pkt[i]))
        if (i + 1) % 16 == 0:
            sys.stdout.write("\n")
        elif (i + 1) % 8 == 0:
            sys.stdout.write("  ")
    sys.stdout.write("\n")


def checksum(pkt: bytes) -> int:
    """Calculate checksum"""
    csum = 0
    count = 0
    count_to = (len(pkt) // 2) * 2

    while count < count_to:
        this_val = (pkt[count + 1]) * 256 + (pkt[count])
        csum = csum + this_val
        csum = csum & 0xFFFFFFFF
        count = count + 2

    if count_to < len(pkt):
        csum = csum + (pkt[len(pkt) - 1])
        csum = csum & 0xFFFFFFFF

    csum = (csum >> 16) + (csum & 0xFFFF)
    csum = csum + (csum >> 16)
    result = ~csum
    result = result & 0xFFFF
    result = result >> 8 | (result << 8 & 0xFF00)

    return result


def parse_reply(my_socket: socket.socket, req_id: int, timeout: int, addr_dst: str) -> tuple:
    """Receive an Echo reply"""
    time_left = timeout
    while True:
        started_select = time.time()
        what_ready = select.select([my_socket], [], [], time_left)
        how_long_in_select = time.time() - started_select
        if what_ready[0] is []:  # Timeout
            raise TimeoutError("Request timed out after 1 sec")

        time_rcvd = time.time()
        time_tot = time_rcvd - time_left
        time_tot = round(time_tot % 1000, 2)
        pkt_rcvd, addr = my_socket.recvfrom(1024)
        # if addr[0] != addr_dst:
        #     raise ValueError("Wrong sender: {}".format(addr[0]))
        # TODO: Extract ICMP header from the IP packet and parse it
        length = len(pkt_rcvd)
        ttl = pkt_rcvd[24]
        # print_raw_bytes(pkt_rcvd)
        if pkt_rcvd[6:7] != b'\x00':
            raise ValueError("Type Error")
        # DONE: End of ICMP parsing
        time_left = time_left - how_long_in_select
        if time_left <= 0:
            raise TimeoutError("Request timed out after 1 sec")
        return addr[0], addr_dst, length, ttl, time_tot


def format_request(req_id: int, seq_num: int) -> bytes:
    """Format an Echo request"""
    my_checksum = 0
    header = struct.pack(
        "bbHHh", ECHO_REQUEST_TYPE, ECHO_REQUEST_CODE, my_checksum, req_id, seq_num
    )
    data = struct.pack("d", time.time())
    my_checksum = checksum(header + data)

    if sys.platform == "darwin":
        my_checksum = socket.htons(my_checksum) & 0xFFFF
    else:
        my_checksum = socket.htons(my_checksum)

    header = struct.pack(
        "bbHHh", ECHO_REQUEST_TYPE, ECHO_REQUEST_CODE, my_checksum, req_id, seq_num
    )
    packet = header + data
    return packet


def send_request(addr_dst: str, seq_num: int, timeout: int = 1) -> tuple:
    """Send an Echo Request"""
    result = None
    proto = socket.getprotobyname("icmp")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, proto)
    my_id = os.getpid() & 0xFFFF

    packet = format_request(my_id, seq_num)
    my_socket.sendto(packet, (addr_dst, 1))

    try:
        result = parse_reply(my_socket, my_id, timeout, addr_dst)
    except ValueError as ve:
        print("Packet error: {}".format(ve))
    finally:
        my_socket.close()
    return result


def ping(host: str, pkts: int, timeout: int = 1) -> None:
    """Main loop"""
    # TODO: Implement the main loop
    t = 1
    tim = []
    rec = 0
    for i in range(pkts):
        addr, addr_dst, length, ttl, time_tot = send_request(host, t)
        if t == 1:
            print("--- Ping {} ({}) using Python ---".format(addr_dst, addr))
        if ttl != 0:
            print("{} bytes from {}: icmp_seq={} TTL={} time={} ms".format(length, addr, t, ttl, time_tot))
            rec += 1
        if ttl == 0:
            print("No response: Request timed out after 1 sec")
        tim.append(time_tot)
        if t == 5:
            print("\n --- {} ping statistics ---".format(addr_dst))
            loss = 100 - (rec/5 * 100)
            if loss != 0:
                print("5 packets transmitted, {} recieved, {}% packet loss".format(rec, loss))
            else:
                print("5 packets transmitted, {} recieved, {}% packet loss".format(rec, loss))
                minl = round(min(tim), 3)
                avgl = round(sum(tim) / float(len(tim)), 3)
                maxl = round(max(tim), 3)
                mdev = round(statistics.stdev(tim), 3)
                print("rtt min/avg/max/mdev = {}/{}/{}/{} ms".format(minl, avgl, maxl, mdev), "\n")
        t += 1

    # DONE
    # return


if __name__ == "__main__":
    for rir in REGISTRARS:
        ping(rir, 5)
