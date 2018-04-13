import getpass
import sys
import ssl
import socket


def create_connection(host, port):
    try:
        sock = ssl.wrap_socket(socket.create_connection((host, port), 1.25))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(get_line(sock), end='')
        return sock
    except ConnectionError as exception:
        sys.exit(exception)
    except socket.gaierror as exception:
        sys.exit(exception)
    except socket.timeout as exception:
        sys.exit(exception)


def send_cmd(sock, cmd):
    sock.sendall(cmd.encode())
    return get_resp(sock).decode()


def get_line(sock):
    return sock.recv(8192).decode()


def get_resp(sock, buffsize=8192):
    resp = []
    while 1:
        try:
            data = sock.recv(buffsize)
        except socket.timeout:
            data = b''
        resp.append(data)
        if not data:
            break
    return b''.join(resp)


def login(sock):
    username = input('> Username: ')
    passwd = getpass.getpass('> Password: ')
    print(send_cmd(sock, f'user {username}\r\n'), end='')
    resp = send_cmd(sock, f'pass {passwd}\r\n')
    if resp.startswith('-ERR') or not resp:
        sys.exit('Authorization failed.')
    else:
        print(resp, end='')


def top(sock, i, n):
    print(send_cmd(sock, f'top {i} {n}\r\n'), end='')


def retr(sock, i):
    with open(f'msg{i}.txt', 'w', encoding='utf-8') as fd:
        print(send_cmd(sock, f'retr {i}\r\n'), file=fd)


if __name__ == '__main__':
    sock = create_connection('pop.mail.ru', 995)
    login(sock)
    retr(sock, 183)
    print(send_cmd(sock, 'quit\r\n'))
"""
6. Стоимость = 10 баллов. POP3 клиент. Пользователю было послано письмо (на русском или
английском языках) на почтовый сервер mail, yandex или rambler. В письмо было сделано
вложение, например, картинка.
Пользователь запускает программу для скачивания письма с почтового сервера. Может запро-
сить заголовки: тему, дату, отправителя и т. п. Может запросить TOP (несколько строк) сооб-
щения. Может скачать письмо с вложением.
"""
