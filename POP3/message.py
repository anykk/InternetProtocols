import base64
import re


SUBJECT = re.compile(r"(?m)^Subject: (.+)$")


if __name__ == '__main__':
    with open('msg183.txt') as fd:
        print(SUBJECT.findall(fd.read()))
