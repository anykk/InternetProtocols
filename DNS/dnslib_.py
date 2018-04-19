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
    return bitstring.pack('uint:16, uint:1, uint:4, 4*uint:1, uint:3, uint:4, 4*uint:16',
                          *header._asdict().values()).tobytes()


Question = namedtuple('Question', ['QNAME', 'QTYPE', 'QCLASS'])


def _question_frombytes(bs: bitstring.Bits, index):
    qname, index = name_frombytes(bs, index)
    qtype = bs[index: index + 16].uint
    qclass = bs[index + 16: index + 32].uint
    return Question(qname, qtype, qclass), index + 32


def questions_frombytes(bs: bitstring.Bits, index, count):
    questions = []
    for _ in range(count):
        question, index = _question_frombytes(bs, index)
        questions.append(question)
    questions.append(index)
    return tuple(questions)


def questions_tobytes(questions):
    bytes_ = []
    for question in questions:
        bytes_.append(name_tobytes(question.QNAME))
        bytes_.append(bitstring.pack('2*uint:16', question.QTYPE, question.QCLASS).tobytes())
    return b''.join(bytes_)


def name_frombytes(bs: bitstring.Bits, index):
    name = ''
    part_length = bs[index: index + 8].uint
    while part_length != 0:
        if part_length >= 192:
            pointer = bs[index + 2: index + 16].uint * 8  # shift
            name += name_frombytes(bs, pointer)[0]
            return name, index + 16
        else:
            index += 8
            for i in range(part_length):
                name += bs[index: index + 8].bytes.decode(errors='ignore')
                index += 8
            name += '.'
        part_length = bs[index: index + 8].uint
    return name[:-1], index + 8


def name_tobytes(name):
    name_parts = []
    for name_part in name.split('.'):
        name_parts.append(bitstring.pack('uint:8', len(name_part)).bytes)
        name_parts.append(name_part.encode())
    name_parts.append(bitstring.pack('uint:8', 0).bytes)
    return b''.join(name_parts)


ResourceRecord = namedtuple('ResourceRecord', ['NAME', 'TYPE', 'CLASS', 'TTL', 'RDLENGTH', 'RDATA'])


def rr_frombytes(bs: bitstring.Bits, index):
    name, index = name_frombytes(bs, index)
    type_ = bs[index: index + 16].uint
    class_ = bs[index + 16: index + 32].uint
    ttl = bs[index + 32: index + 64].uint  # seconds
    rdlength = bs[index + 64: index + 80].uint
    rdata, index = rdata_frombytes(bs, index + 80, rdlength, type_)
    return ResourceRecord(name, type_, class_, ttl, rdlength, rdata), index


def rrs_frombytes(bs: bitstring.Bits, index, count):
    rrs = []
    if count > 0:
        for _ in range(count):
            rr, index = rr_frombytes(bs, index)
            rrs.append(rr)
    rrs.append(index)
    return tuple(rrs)


def rrs_tobytes(rrs):
    bytes_ = []
    for rr in rrs:
        name = name_tobytes(rr.NAME)
        rdata = rdata_tobytes(rr.RDATA, rr.TYPE)
        fields = bitstring.pack('2*uint: 16, uint: 32, uint: 16',
                                rr.TYPE, rr.CLASS, rr.TTL, len(rdata)).bytes
        bytes_ += [name, fields, rdata]
    return b''.join(bytes_)


def rdata_tobytes(rdata, type_):
    if type_ == 1:
        address = bitstring.BitArray()
        address_parts = rdata.split('.')
        i = 0
        for parts in address_parts:
            address[i:i + 8] = bitstring.pack('uint: 8', int(parts))
            i += 8
        return address.tobytes()
    elif type_ == 2 or type_ == 5:
        return name_tobytes(rdata)
    else:
        raise UnsupportedTypeError(f"type {type_} hasn't supported.")


def rdata_frombytes(bs: bitstring.Bits, index, length, type_):  # A & NS
    if type_ == 1:
        address = ''
        for i in range(length):
            address += str(bs[index:index + 8].uint)
            index += 8
            address += '.'
        return address[:-1], index
    elif type_ == 2 or type_ == 5:
        address, index = name_frombytes(bs, index)
        return address, index
    else:
        raise UnsupportedTypeError(f"type {type_} not supported.")


DNSPacket = namedtuple('DNSPacket', ['Header', 'Question', 'Answer', 'Authority', 'Additional'])


def _section_frombytes(f, bs: bitstring.Bits, index, count):
    if count > 0:
        section = f(bs, index, count)
        return section[:-1], section[-1]
    else:
        return tuple(), index


def packet_frombytes(bs: bitstring) -> DNSPacket:
    try:
        header = header_frombytes(bs)
        index = 96
        question, index = _section_frombytes(questions_frombytes, bs, index, header.QDCOUNT)
        answer, index = _section_frombytes(rrs_frombytes, bs, index, header.ANCOUNT)
        authority, index = _section_frombytes(rrs_frombytes, bs, index, header.NSCOUNT)
        additional, _ = _section_frombytes(rrs_frombytes, bs, index, header.ARCOUNT)
        return DNSPacket(header, question, answer, authority, additional)
    except bitstring.Error:
        raise DNSParseError("bad packet. couldn't parse")


def packet_tobytes(packet: DNSPacket) -> bytes:
    try:
        header = header_tobytes(packet.Header)
        question = questions_tobytes(packet.Question)
        answer = rrs_tobytes(packet.Answer)
        authority = rrs_tobytes(packet.Authority)
        additional = rrs_tobytes(packet.Additional)
        return b''.join([header, question, answer, authority, additional])
    except bitstring.Error:
        raise DNSParseError("couldn't encode packet. bad fields")


class DNSError(Exception): pass
class UnsupportedTypeError(DNSError): pass
class DNSParseError(DNSError): pass
