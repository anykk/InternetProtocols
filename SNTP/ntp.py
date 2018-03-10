import bitstring
import datetime
import time
import pprint


class NTPPacket:
    """SNTP packet class."""

    def __init__(self, vn=4, mode=3, transmit_timestamp=0):
        self.__li = 0  # Leap Indicator: 3 at first and the last; 0/1/2 - 2bit uInt
        self.__vn = vn  # Version Number: currently 4 - 3bit uInt
        self.__mode = mode  # 3/4/5 [C/S/bS] - 3bit uInt
        self.__stratum = 0  # 0/1/2-15/[reserved]16-255 - 8bit uInt
        self.__poll = 0  # Poll Interval: range[4 (16 s), 17 (131,072 s ~ about 36 h)] - 8bit uInt
        self.__precision = 0  # 8bit sInt
        self.__root_delay = 0  # 32bit sFixed-Point with the fraction point between bits 15&16
        self.__root_dispersion = 0  # 32bit uFixed-Point with the fraction point between bits 15&16
        self.__reference_id = 0  # 32bit bitstring [stratum 0 & 1: 4chrASCII str left justified & 0 padded]
        self.__reference_timestamp = 0  # \
        self.__originate_timestamp = 0  # \
        # time in 64bit timestamp format
        self.__receive_timestamp = 0  # /
        self.__transmit_timestamp = transmit_timestamp  # /
        # Authenticator (optional): Key Identifier(32bit) & Message Digest(128bit)

    def from_data(self, data):
        bs = bitstring.Bits(data)
        self.__li = bs[0:2].uint
        self.__vn = bs[2:5].uint
        self.__mode = bs[5:8].uint
        self.__stratum = bs[8:16].uint
        self.__poll = bs[16:24].uint
        self.__precision = 2 ** bs[24:32].int
        self.__root_delay = bs[32:64].int / 65536.0
        self.__root_dispersion = bs[64:96].uint / 65536.0
        self.__reference_id = tuple(bs[96:128].unpack('4*uint:8'))
        self.__reference_timestamp = None
        self.__originate_timestamp = None
        self.__receive_timestamp = None
        self.__transmit_timestamp = None

    def __str__(self):
        return f'LI: {self.__li}\n' \
               f'VN: {self.__vn}\n' \
               f'Mode: {self.__mode}\n' \
               f'Stratum: {self.__stratum}\n' \
               f'Poll: {self.__poll}\n' \
               f'Precision: {round(self.__precision, 6)} sec\n' \
               f'Root Delay: {self.__root_delay} seconds\n' \
               f'Root Dispersion: {self.__root_dispersion} seconds\n' \
               f'Reference Identifier: {".".join(map(lambda x: str(x), self.__reference_id))}\n' \
               f'Reference Timestamp: {self.__reference_timestamp}\n' \
               f'Originate Timestamp: {self.__originate_timestamp}\n' \
               f'Receive Timestamp: {self.__receive_timestamp}\n' \
               f'Transmit Timestamp: {self.__transmit_timestamp}'


if __name__ == '__main__':
    p = NTPPacket()
    p.from_data(b'\x1c\x02\x00\xe9\x00\x00\x1eh\x00\x00\x05\x82\x80\x8a\x8d\xac\xdeNUw\xb1S\x9d6\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\xdeNVi\x89c\xdf\xa3\xdeNVi\x89d\x11\xf8')
    print(str(p))
