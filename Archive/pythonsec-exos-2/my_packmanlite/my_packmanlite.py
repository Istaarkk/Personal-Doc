import struct

def ushort_uint(buf):
    if len(buf) <6:
        raise ValueError ("Le buffer doit au moins etre de 6")
    return struct.unpack('>HI', buf[:6])

def buf2latin(buf):
    size = struct.unpack('>H', buf[:2])[0]
    string = buf[2:2+size].decode('latin-1') 
    return size, string

def ascii2buf(*args):
    total_len = len(args)

    buffer = bytearray()

    buffer.extend(struct.pack('>I', total_len))

    for string in args:
        buffer.extend(struct.pack('>H', len(string))) 
        buffer.extend(string.encode('ascii'))

    return buffer
