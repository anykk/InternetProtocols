import sys
import argparse
import socket
import sntp
import time
import random


REF_ID = 'LOCL'.encode('ascii')


def mode_to_reply(mode):
    if mode == 3:
        return 4
    elif mode == 1:
        return 2


def parse_args():
    parser = argparse.ArgumentParser(description='simple sntp server implementation')
    parser.add_argument('lie', nargs='?', default=0, type=int, help='seconds to lie')
    return parser.parse_args()


def main():
    args = parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 123))
        print('Server was started')
        while 1:
            try:
                data, addr = sock.recvfrom(8192)
                recv_time = time.time() + args.lie
                print(f'Handle connection from: {addr}')
                request = sntp.SNTPPacket()
                request.from_bytes(data)
                print(f"Client's request:\n{str(request)}")
                trans_time = time.time() + args.lie
                sock.sendto(sntp.SNTPPacket(vn=request.vn,
                                            mode=mode_to_reply(request.mode),
                                            stratum=1,
                                            poll=request.poll,
                                            ref_id=REF_ID,
                                            reference_timestamp=time.time() - random.randint(1, 2**16) + args.lie,
                                            originate_timestamp=request.transmit_timestamp + args.lie,
                                            receive_timestamp=recv_time,
                                            transmit_timestamp=trans_time).to_bytes(), addr)

            except KeyboardInterrupt:
                sys.exit()
            except Exception as exception:
                print(str(exception), file=sys.stderr)


if __name__ == '__main__':
    try:
        main()
    except Exception as exception:
        sys.exit(exception)
