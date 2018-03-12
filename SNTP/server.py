import sys
import argparse
import socket
import sntp
import time


def parse_args():
    parser = argparse.ArgumentParser(description='simple sntp server implementation')
    parser.add_argument('host', nargs='?', default='localhost', type=str, help='host to serve')
    parser.add_argument('port', nargs='?', default=123, type=int, help='port to serve')
    parser.add_argument('lie', nargs='?', default=60, type=int, help='seconds to lie')
    return parser.parse_args()


def get_ref_id(sock):
    return tuple(map(lambda x: int(x), sock.getsockname()[0].split('.')))


def main():
    args = parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 123))
        while 1:
            try:
                data, addr = sock.recvfrom(8192)
                print(f'Handle connection from: {addr}')
                request = sntp.SNTPPacket()
                request.from_bytes(data)
                print(f"Client's request:\n{str(request)}")
                response = sntp.SNTPPacket(originate_timestamp=request.transmit_timestamp,
                                           receive_timestamp=time.time() + args.lie, transmit_timestamp=time.time(),
                                           stratum=2, mode=4, ref_id=get_ref_id(sock))
                sock.sendto(response.to_bytes(), addr)
            except sntp.SNTPException as exception:
                print(exception, file=sys.stderr)
            except Exception as exception:
                sys.exit(exception)


if __name__ == '__main__':
    main()
