import socket
from dnslib_ import *
from time import time
import pickle
from pprint import pprint


def load_cache():
    try:
        with open('cache.pickle', 'rb') as f:
            cache = pickle.load(f)
            return cache
    except OSError:
        print('Failed to read cache.')
        return dict()


def store_cache(cache):
    try:
        with open('cache.pickle', 'wb') as f:
            pickle.dump(cache, f)
    except OSError:
        print('Failed to store cache.')


def main():
    def add_entry(p):
        cache[(p.Question[0].QNAME, p.Question[0].QTYPE)] = (p, time() + p.Answer[0].TTL)

    def get_entry(p):
        e = cache.get((p.Question[0].QNAME, p.Question[0].QTYPE), None)
        del_expired()
        return e[0] if e is not None else None

    def del_expired():
        expired = []
        for k, v in cache.items():
            if v[1] < time():
                expired.append(k)
        for k in expired:
            del cache[k]

    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('localhost', 53))

        query_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        cache = load_cache()

        while True:
            query, addr = server_sock.recvfrom(1024)
            packet = packet_frombytes(bitstring.Bits(query))
            pprint(f'Request from: {addr}')
            pprint(packet._asdict(), indent=2)

            entry = get_entry(packet)
            if not entry:
                print('Cache MISS')

                query_sock.connect(('8.8.8.8', 53))
                query_sock.sendall(packet_tobytes(packet))
                answer = query_sock.recv(1024)

                anspacket = packet_frombytes(bitstring.Bits(answer))

                add_entry(anspacket)

                pprint(f'Answer for: {addr}')
                pprint(anspacket._asdict(), indent=2)
            else:
                print('Cache HIT')

                header = Header(packet.Header.ID, *entry.Header[1:])
                anspacket = DNSPacket(header, *entry[1:])

                pprint(anspacket._asdict(), indent=2)

            server_sock.sendto(packet_tobytes(anspacket), addr)
    except (KeyboardInterrupt, Exception):
        store_cache(cache)
        print('Bye.')


if __name__ == '__main__':
    main()
