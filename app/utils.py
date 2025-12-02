def encode_as_bulk_string(value):
    len_string = len(value)
    bytestr_len_string = str(len_string).encode()
    bulk_string = b"$"+ bytestr_len_string + b"\r\n" + value + b"\r\n"
    return bulk_string

def encode_as_simple_string(value):
    return b"+" + value + b"\r\n"