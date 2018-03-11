"""SNTPv3 client for test."""
import sntp
import socket


NTP_SERVER = 'localhost'


def get_time():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = sntp.SNTPPacket().to_bytes()
    client.sendto(data, (NTP_SERVER, 123))
    data, address = client.recvfrom(1024)
    if data:
        print('Response received from:', address)
    response = sntp.SNTPPacket()
    response.from_bytes(data)
    print(str(response))


if __name__ == '__main__':
    get_time()
