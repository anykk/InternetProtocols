import socket
from dnslib_ import *
from cache import *


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 53))

    query_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    query_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    cache = Cache('dns_cache')

    while True:
        query, addr = server_sock.recvfrom(1024)
        packet = packet_frombytes(bitstring.Bits(query))

        query_sock.connect(('e1.ru.', 53))
        query_sock.sendall(packet_tobytes(packet))
        answer = query_sock.recv(1024)
        anspacket = packet_frombytes(bitstring.Bits(answer))

        server_sock.sendto(packet_tobytes(anspacket), addr)


if __name__ == '__main__':
    main()

