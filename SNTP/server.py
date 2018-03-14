import sys
import argparse
import socket
import sntp
import time


def parse_args():
    """Just arg's parse."""
    parser = argparse.ArgumentParser(description='simple sntp server implementation')
    parser.add_argument('lie', nargs='?', default=60, type=int, help='seconds to lie')
    return parser.parse_args()


def main():
    args = parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 123))
        while 1:
            data, addr = sock.recvfrom(8192)
            recv_t = time.time() + args.lie
            print(f'Handle connection from: {addr}')
            request = sntp.SNTPPacket()
            request.from_bytes(data)
            print(f"Client's request:\n{str(request)}")
            sock.sendto(sntp.SNTPPacket(vn=request.vn, stratum=1, originate_timestamp=request.transmit_timestamp,
                                        receive_timestamp=recv_t, transmit_timestamp=time.time()).to_bytes(), addr)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as exception:
        sys.exit(exception)
