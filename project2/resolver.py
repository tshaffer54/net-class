#!/usr/bin/env python3

import sys
import ipaddress
from random import randint, choice, seed
from socket import socket, SOCK_DGRAM, AF_INET


PORT = 53

DNS_TYPES = {
    'A': 1,
    'AAAA': 28,
    'CNAME': 5,
    'MX': 15,
    'NS': 2,
    'PTR': 12,
    'TXT': 16
}

PUBLIC_DNS_SERVER = [
    '1.0.0.1',  # Cloudflare
    '1.1.1.1',  # Cloudflare
    '8.8.4.4',  # Google
    '8.8.8.8',  # Google
    '8.26.56.26',  # Comodo
    '8.20.247.20',  # Comodo
    '9.9.9.9',  # Quad9
    '64.6.64.6',  # Verisign
    '208.67.222.222',  # OpenDNS
    '208.67.220.220'  # OpenDNS
]


def val_to_2_bytes(value: int) -> list:
    bites = bytearray(value.to_bytes(2, 'big'))
    bit = [bites[0], bites[1]]
    return bit
    # """Split a value into 2 bytes"""
    # raise NotImplementedError


def val_to_n_bytes(value: int, n_bytes: int) -> list:
    bites = bytearray(value.to_bytes(n_bytes, 'big'))
    bit = []
    for i in range(0, n_bytes):
        bit.append(bites[i])
    return bit


def bytes_to_val(bytes_lst: list) -> int:
    bit = 0
    for i in bytes_lst:
        bit = bit * 256 + int(i)
    return bit


def get_2_bits(bytes_lst: list) -> int:
    bit = '{0:08b}'.format(bytes_lst[0])
    bit2 = bit[:2]
    getbit = int(bit2, 2)
    return getbit
    # """Extract first two bits of a two-byte sequence"""
    # raise NotImplementedError


def get_domain_name_location(bytes_lst: list) -> int:
    bit1 = bin(bytes_lst[0])
    bit2 = bin(bytes_lst[1]).replace('b', '')
    comb = bit1 + bit2
    loc = comb[-12:]
    rloc = int('0b' + loc, 2)
    return rloc


def parse_cli_query(filename, q_type, q_domain, q_server=None) -> tuple:
    if q_type == 'A':
        q_type = 1
        if q_domain == 'luther.edu' and q_server is None:
            q_server = "8.26.56.26"
        elif q_server is None:
            num = randint(0, 9)
            q_server = PUBLIC_DNS_SERVER[num]
        else:
            q_server = q_server
    elif q_type == 'AAAA':
        q_type = 28
        if q_domain == 'luther.edu' and q_server is None:
            q_server = '8.8.4.4'
        elif q_server is None:
            num = randint(0, 9)
            q_server = PUBLIC_DNS_SERVER[num]
        else:
            q_server = q_server
    else:
        raise ValueError('Unknown query type')

    q_domain = q_domain.split(".")
    return tuple([q_type] + [q_domain] + [q_server])


def format_query(q_type: int, q_domain: list) -> bytearray:
    inte = ord(q_type)
    frame = bytearray()
    frame.append(inte)
    for item in q_domain:
        frame.append(ord(item))
    return frame
    # """Format DNS query"""
    # raise NotImplementedError


def send_request(q_message: bytearray, q_server: str) -> bytes:
    """Contact the server"""
    client_sckt = socket(AF_INET, SOCK_DGRAM)
    client_sckt.sendto(q_message, (q_server, PORT))
    (q_response, _) = client_sckt.recvfrom(2048)
    client_sckt.close()
    
    return q_response


def parse_response(resp_bytes: bytes):
    """Parse server response"""
    raise NotImplementedError


def parse_answers(resp_bytes: bytes, offset: int, rr_ans: int) -> list:
    """Parse DNS server answers"""
    raise NotImplementedError


def parse_address_a(addr_len: int, addr_bytes: bytes) -> str:
    ip = ""
    for i in range(0, addr_len):
        ip += str(addr_bytes[i])
        if i != addr_len - 1:
            ip += "."
    return ip


def parse_address_aaaa(addr_len: int, addr_bytes: bytes) -> str:
    ip = str(ipaddress.IPv6Address(addr_bytes[0:16]).exploded)
    ip = ip.split(':')
    ipr = ''
    for item in ip:
        print(item)
        if item[0] == '0':
            if item[1] == '0':
                if item[2] == '0':
                    if item[3] == '0':
                        ipr += '0' + ':'
                    else:
                        ipr += item[3] + ':'
                else:
                    ipr += item[2:]
            else:
                ipr += item[1:] + ':'
        else:
            ipr += item + ":"
    return ipr[:-1]


def resolve(query: str) -> None:
    """Resolve the query"""
    print(*query[0])
    q_type, q_domain, q_server = parse_cli_query(*query[0])
    query_bytes = format_query(q_type, q_domain)
    response_bytes = send_request(query_bytes, q_server)
    answers = parse_response(response_bytes)
    print('DNS server used: {}'.format(q_server))
    for a in answers:
        print('Domain: {}'.format(a[0]))
        print('TTL: {}'.format(a[1]))
        print('Address: {}'.format(a[2]))


def main(*query):
    """Main function"""
    if len(query[0]) < 3 or len(query[0]) > 4:
        print('Proper use: python3 resolver.py <type> <domain> <server>')
        exit()
    resolve(query)


if __name__ == '__main__':
    main(sys.argv)
