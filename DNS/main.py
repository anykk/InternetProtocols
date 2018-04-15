import binascii
import socket
from dnslib_ import *
from pprint import pprint

bs = bitstring.Bits(b'\xaa\xaa\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01\xc0\x0c'
                    b'\x00\x01\x00\x01\x00\x009S\x00\x04]\xb8\xd8"')

print(bs.bytes)
header = header_frombytes(bs)
pprint(header)
pprint(header_tobytes(header))
