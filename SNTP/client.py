import sntp
import socket


NTP_SERVER = 'localhost'


def get_time():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    data = sntp.SNTPPacket().to_bytes()
    client.sendto(data, (NTP_SERVER, 123))
    data, address = client.recvfrom(1024)
    if data:
        print('Response received from:', address)
    response = sntp.SNTPPacket()
    response.from_bytes(data)
    print(f"Server's response:\n{str(response)}")


if __name__ == '__main__':
    get_time()
