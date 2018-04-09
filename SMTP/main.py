import base64
import socket
import ssl


def main():
    msg = """From: dmitriypirozhok@yandex.ru
    To: dmitriypirozhok@yandex.ru
    Subject: privetik
    MIME-Version: 1.0
    Content-Type: text; charset="utf-8"
    
    kajsdhkjqwhdkjnsakdnjkasdxxxxxlizavetkabukaxxxxxxxxxxxasdasdasdkajsd
    .
""".encode()
    sock = socket.socket()
    sock.settimeout(1.25)
    sock = ssl.wrap_socket(sock)
    sock.connect(('smtp.yandex.ru', 465))
    print(recv_all(sock).decode())
    login = base64.encodebytes('dmitriypirozhok@yandex.ru'.encode())
    passw = base64.encodebytes('asd123456'.encode())
    print(send_cmd(sock, 'ehlo dmitriypirozhok\r\n'.encode()))
    print(send_cmd(sock, 'auth login\r\n'.encode() + login + passw))
    print(send_cmd(sock, 'mail from:<dmitriypirozhok@yandex.ru>\r\n'.encode()))
    print(send_cmd(sock, 'rcpt to:<dmitriypirozhok@yandex.ru>\r\n'.encode()))
    print(send_cmd(sock, 'data\n'.encode()))
    print(send_cmd(sock, msg))
    #  print(send_cmd(sock, 'noop\r\n'.encode()))
    #  print(send_cmd(sock, 'kirill.yldashev@mail.ru\r\n'.encode()))


def send_cmd(sock, cmd):
    sock.sendall(cmd)
    return recv_all(sock).decode()


def recv_all(sock, buff_size=1024):
    resp = []
    while 1:
        try:
            data = sock.recv(buff_size)
        except socket.timeout:
            data = b''
        resp.append(data)
        if not data:
            break
    return b''.join(resp)


if __name__ == '__main__':
    main()
