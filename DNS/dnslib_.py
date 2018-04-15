import bitstring
from collections import namedtuple

Header = namedtuple('Header', ['ID', 'QR', 'Opcode', 'AA', 'TC',
                               'RD', 'RA', 'Z', 'RCODE', 'QDCOUNT',
                               'ANCOUNT', 'NSCOUNT', 'ARCOUNT'])


def header_frombytes(bs: bitstring.Bits) -> Header:
    return Header(bs[0:16].uint, bs[16:17].uint, bs[17:21].uint, bs[21:22].uint, bs[22:23].uint,
                  bs[23:24].uint, bs[24:25].uint, bs[25:28].uint, bs[28:32].uint, bs[32:48].uint,
                  bs[48:64].uint, bs[64:80].uint, bs[80:96].uint)


def header_tobytes(header: Header) -> bytes:
    return bitstring.pack('uint:16, 7*uint:1, uint:4, 4*uint:16', *header._asdict().values()).tobytes()
