import sys
import socket
import sntp
import time


def get_ref_id(sock):
    return tuple(map(lambda x: int(x), sock.getsockname()[0].split('.')))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', 123))
        while 1:
            try:
                data, addr = sock.recvfrom(8192)
                request = sntp.SNTPPacket()
                request.from_bytes(data)
                response = sntp.SNTPPacket(originate_timestamp=request.transmit_timestamp,
                                           receive_timestamp=time.time() + 0, transmit_timestamp=time.time(),
                                           stratum=2, mode=4, ref_id=get_ref_id(sock))
                sock.sendto(response.to_bytes(), addr)
            except sntp.SNTPException as e:
                print(e)
            except Exception as e:
                sys.exit(e)


if __name__ == '__main__':
    main()
