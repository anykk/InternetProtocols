"""SNTP tools."""
import bitstring
import datetime

TIME1970 = 2208988800

REF_ID_TABLE = {
    'DNC': "DNC routing protocol",
    'NIST': "NIST public modem",
    'TSP': "TSP time protocol",
    'DTS': "Digital Time Service",
    'ATOM': "Atomic clock (calibrated)",
    'VLF': "VLF radio (OMEGA, etc)",
    'callsign': "Generic radio",
    'LORC': "LORAN-C radionavidation",
    'GOES': "GOES UHF environment satellite",
    'GPS': "GPS UHF satellite positioning",
}

STRATUM_TABLE = {
    0: "kiss-o'-death message",
    1: "primary reference",
}

MODE_TABLE = {
    0: "unspecified",
    1: "symmetric active",
    2: "symmetric passive",
    3: "client",
    4: "server",
    5: "broadcast",
    6: "reserved for NTP control messages",
    7: "reserved for private use",
}

LEAP_TABLE = {
    0: "no warning",
    1: "last minute has 61 seconds",
    2: "last minute has 59 seconds",
    3: "alarm condition (clock not synchronized)",
}


class SNTPException(Exception):
    """SNTP exception."""
    pass


class SNTPPacket:
    """SNTPv3 packet class.

    Mode 3 cause it works only with IPv4.
    ...full docstring will be here..."""

    def __init__(self, li=0,
                 vn=3, mode=3,
                 stratum=0, poll=0,
                 precision=0, delay=0,
                 dispersion=0,
                 ref_id=(0, 0, 0, 0),
                 reference_timestamp=0,
                 originate_timestamp=0,
                 receive_timestamp=0,
                 transmit_timestamp=0):
        """Initialize the SNTPv3 (by default) packet."""
        self.__li = li
        self.__vn = vn
        self.__mode = mode
        self.__stratum = stratum
        self.__poll = poll
        self.__precision = precision
        self.__root_delay = _to1616(delay)
        self.__root_dispersion = _to1616(dispersion)
        self.__reference_id = ref_id
        self.__reference_timestamp = _to_timestamp(reference_timestamp)
        self.__originate_timestamp = _to_timestamp(originate_timestamp)
        self.__receive_timestamp = _to_timestamp(receive_timestamp)
        self.__transmit_timestamp = _to_timestamp(transmit_timestamp)

    @property
    def li(self):
        return self.__li

    @property
    def vn(self):
        return self.__vn

    @property
    def mode(self):
        return self.__mode

    @property
    def stratum(self):
        return self.__stratum

    @property
    def poll(self):
        return self.__poll

    @property
    def precision(self):
        return self.__precision

    @property
    def root_delay(self):
        return self.__root_delay

    @property
    def root_dispersion(self):
        return self.__root_dispersion

    @property
    def reference_id(self):
        return self.__reference_id

    @property
    def reference_timestamp(self):
        return self.__reference_timestamp

    @property
    def origin_timestamp(self):
        return self.__reference_timestamp

    @property
    def receive_timestamp(self):
        return self.__receive_timestamp

    @property
    def transmit_timestamp(self):
        return self.__transmit_timestamp

    def from_bytes(self, data):
        """Decode data and set up packet fields if we can."""
        bs = bitstring.Bits(data)
        if len(bs) < 48:
            raise SNTPException('invalid SNTP packet.')
        self.__li = bs[0:2].uint
        self.__vn = bs[2:5].uint
        self.__mode = bs[5:8].uint
        self.__stratum = bs[8:16].uint
        self.__poll = bs[16:24].uint
        self.__precision = bs[24:32].int
        self.__root_delay = _from1616(bs[32:64].int)
        self.__root_dispersion = _from1616(bs[64:96].uint)
        self.__reference_id = tuple(bs[96:128].unpack('4*uint: 8'))
        self.__reference_timestamp = _from_timestamp(bs[128:192].uint)
        self.__originate_timestamp = _from_timestamp(bs[192:256].uint)
        self.__receive_timestamp = _from_timestamp(bs[256:320].uint)
        self.__transmit_timestamp = _from_timestamp(bs[320:384].uint)

    def to_bytes(self):
        """Encode packet to utf-8 byte sequence."""
        bs = bitstring.BitArray(length=384)
        bs[0:2] = bitstring.pack('uint: 2', self.__li)
        bs[2:5] = bitstring.pack('uint: 3', self.__vn)
        bs[5:8] = bitstring.pack('uint: 3', self.__mode)
        bs[8:16] = bitstring.pack('uint: 8', self.__stratum)
        bs[16:24] = bitstring.pack('uint: 8', self.__poll)
        bs[24:32] = bitstring.pack('int: 8', self.__precision)
        bs[32:64] = bitstring.pack('int: 32', self.__root_delay)
        bs[64:96] = bitstring.pack('int: 32', self.__root_dispersion)
        bs[96:128] = bitstring.pack('4*uint: 8', *self.__reference_id)
        bs[128:192] = bitstring.pack('uint: 64', self.__reference_timestamp)
        bs[192:256] = bitstring.pack('uint: 64', self.__originate_timestamp)
        bs[256:320] = bitstring.pack('uint: 64', self.__receive_timestamp)
        bs[320:384] = bitstring.pack('uint: 64', self.__transmit_timestamp)
        return bs.tobytes()

    def __str__(self):
        """Packet's string representation."""
        return f'LI: {_pretty_li(self.__li)}\n' \
               f'VN: {self.__vn}\n' \
               f'Mode: {_pretty_mode(self.__mode)}\n' \
               f'Stratum: {_pretty_stratum(self.__stratum)}\n' \
               f'Poll: {self.__poll}\n' \
               f'Precision: {round(2 ** self.__precision, 6)} sec\n' \
               f'Root Delay: {self.__root_delay} seconds\n' \
               f'Root Dispersion: {self.__root_dispersion} seconds\n' \
               f'Reference Identifier: {_pretty_ref_id(self.__reference_id, self.__stratum)}\n' \
               f'Reference Timestamp: {_pretty_timestamp(self.__reference_timestamp)}\n' \
               f'Originate Timestamp: {_pretty_timestamp(self.__originate_timestamp)}\n' \
               f'Receive Timestamp: {_pretty_timestamp(self.__receive_timestamp)}\n' \
               f'Transmit Timestamp: {_pretty_timestamp(self.__transmit_timestamp)}'


def _to1616(n):
    """Num to 16.16 fixed-point."""
    return float(n) * 2 ** 16


def _from1616(n):
    """Num from 16.16 fixed-point."""
    return float(n) / 2 ** 16


def _to_timestamp(s):
    """Num to ntp 32.32 timestamp format."""
    return (float(s) + TIME1970) * 2 ** 32 if s != 0 else 0


def _from_timestamp(s):
    """Num from ntp 32.32 timestamp format."""
    return float(s) / 2 ** 32 - TIME1970 if s != 0 else 0


def _pretty_li(li):
    """Leap indicator to pretty string."""
    if li in LEAP_TABLE:
        return f'{li} ({LEAP_TABLE[li]})'
    else:
        raise SNTPException('invalid leap indicator field.')


def _pretty_mode(mode):
    """Mode to pretty string."""
    if mode in MODE_TABLE:
        return f'{mode} ({MODE_TABLE[mode]})'
    else:
        raise SNTPException('invalid mode field.')


def _pretty_stratum(stratum):
    """Stratum to pretty string."""
    if stratum in STRATUM_TABLE:
        return f'{stratum} {(STRATUM_TABLE[stratum])}'
    elif 2 <= stratum <= 15:
        return f'{stratum} (secondary reference)'
    elif 16 <= stratum <= 255:
        return f'{stratum} (reserved)'
    else:
        raise SNTPException('invalid stratum filed.')


def _pretty_ref_id(ref_id, stratum):
    """Reference Identifier to pretty string."""
    if 0 <= stratum <= 1:
        text = '{}{}{}{}'.format(*ref_id)
        if text in REF_ID_TABLE:
            return REF_ID_TABLE[text]
        else:
            return text
    elif 2 <= stratum <= 255:
        return '{}.{}.{}.{}'.format(*ref_id)
    else:
        raise SNTPException('invalid reference identifier flied.')


def _pretty_timestamp(ts):
    """Timestamp to pretty string."""
    try:
        return str(datetime.datetime.utcfromtimestamp(ts)) + ' UTC'
    except OSError:
        raise SNTPException('invalid timestamp.')
