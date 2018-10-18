"""
DNS Name Server
"""
#!/usr/bin/env python3

import sys
from random import randint, choice
from socket import socket, SOCK_DGRAM, AF_INET


HOST = "localhost"
PORT = 43053

DNS_TYPES = {
    1: 'A',
    2: 'NS',
    5: 'CNAME',
    12: 'PTR',
    15: 'MX',
    16: 'TXT',
    28: 'AAAA'
}

TTL_SEC = {
    '1s': 1,
    '1m': 60,
    '1h': 60*60,
    '1d': 60*60*24,
    '1w': 60*60*24*7,
    '1y': 60*60*24*365
    }


def val_to_bytes(value: int, n_bytes: int) -> list:
    bites = bytearray(value.to_bytes(n_bytes, 'big'))
    bit = []
    for i in range(0, n_bytes):
        bit.append(bites[i])
    return bit
    # """Split a value into n bytes"""
    # raise NotImplementedError


def bytes_to_val(bytes_lst: list) -> int:
    bit = 0
    for i in bytes_lst:
        bit = bit * 256 + int(i)
    return bit
    # """Merge n bytes into a value"""
    # raise NotImplementedError


def get_left_bits(bytes_lst: list, n_bits: int) -> int:
    bit1 = bin(bytes_lst[0]).replace('b', '')
    bit2 = bin(bytes_lst[1]).replace('b', '')
    bits = bit1 + bit2
    lbits = bits[:n_bits+1]
    lbit = int(lbits, 2)
    return lbit
    # """Extract left n bits of a two-byte sequence"""
    # raise NotImplementedError


def get_right_bits(bytes_lst: list, n_bits) -> int:
    bit1 = bin(bytes_lst[0])
    bit2 = bin(bytes_lst[1]).replace('b', '')
    bits = bit1 + bit2
    rbits = bits[-n_bits:]
    rbit = int(rbits, 2)
    return rbit
    # """Extract right n bits bits of a two-byte sequence"""
    # raise NotImplementedError


def read_zone_file(filename: str) -> tuple:
    """Read the zone file and build a dictionary"""
    zone = dict()
    with open(filename) as zone_file:
        origin = zone_file.readline().split()[1].rstrip('.')
        ttl1 = zone_file.readline().split()[1]
        for line in zone_file:
            line = line.split()
            if len(line) == 4:
                if TTL_SEC.__contains__(line[0]):
                    dom = list(zone.keys())[-1]
                    domain = dom
                    ttl = line[0]
                    clas = line[1]
                    typ = line[2]
                    addr = line[3]
                    zone[domain].append([ttl, clas, typ, addr])
                else:
                    domain = line[0]
                    ttl = ttl1
                    clas = line[1]
                    typ = line[2]
                    addr = line[3]
                    if zone.__contains__(domain):
                        zone[domain].append([ttl1, clas, typ, addr])
                    else:
                        zone.update({domain: [ttl, clas, typ, addr]})
            elif len(line) == 3:
                dom = list(zone.keys())[-1]
                domain = dom
                clas = line[0]
                typ = line[1]
                addr = line[2]
                ttl = ttl1
                zone[domain].append([ttl, clas, typ, addr])
            else:
                domain = line[0]
                ttl = line[1]
                clas = line[2]
                typ = line[3]
                addr = line[4]
                zone.update({domain: [ttl, clas, typ, addr]})

        # raise NotImplementedError
    return origin, zone


def parse_request(origin: str, msg_req: bytes) -> tuple:
    zone_msg_lst = origin.split('.')
    zone_msg = zone_msg_lst[0]
    trans_id = msg_req[:2]
    trans_idr = int.from_bytes(trans_id, 'big')
    dom = msg_req[13:16]
    dom_name = dom.decode('utf-8')
    query_typ = msg_req[35]
    query = msg_req[12:]
    clas = msg_req[-1:]
    clasr = int.from_bytes(clas, 'big')
    print(type(clasr))
    if zone_msg == 'cs430':
        if query_typ is 1 or query_typ is 28:
            if clasr == 1 or clasr == 28:
                return trans_idr, dom_name, query_typ, query
            else:
                raise ValueError("Unknown class")
        else:
            raise ValueError("Unknown query type")
    else:
        raise ValueError("Unknown zone")
    # """Parse the request"""
    # raise NotImplementedError


def format_response(zone: dict, trans_id: int, qry_name: str, qry_type: int, qry: bytearray) -> bytearray:
    print('blah')
    # """Format the response"""
    # raise NotImplementedError


def run(filename: str) -> None:
    """Main server loop"""
    server_sckt = socket(AF_INET, SOCK_DGRAM)
    server_sckt.connect((HOST, PORT))
    origin, zone = read_zone_file(filename)
    print("Listening on %s:%d" % (HOST, PORT))

    while True:
        (request_msg, client_addr) = server_sckt.recvfrom(512)
        try:
            trans_id, domain, qry_type, qry = parse_request(origin, request_msg)
            msg_resp = format_response(zone, trans_id, domain, qry_type, qry)
            server_sckt.sendto(msg_resp, client_addr)
        except ValueError as ve:
            print('Ignoring the request: {}'.format(ve))
    server_sckt.close()


def main(*argv):
    """Main function"""
    if len(argv[0]) != 2:
        print('Proper use: python3 nameserver.py <zone_file>')
        exit()
    run(argv[0][1])


if __name__ == '__main__':
    main(sys.argv)
