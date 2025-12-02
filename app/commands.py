import time
from .utils import encode_as_bulk_string, encode_as_simple_string

hashmap = {}

NULL_BULK_STRING = b"$-1\r\n"

def handle_command(values):
    command = values[0].upper()
    if command == b"ECHO":
        arg = values[1]
        return encode_as_bulk_string(arg)
    elif command == b"PING":
        return encode_as_simple_string(b"PONG")
    elif command == b"SET":
        return handle_set_command(values)
    elif command == b"GET":
        return handle_get_command(values)

def handle_set_command(values):
    key = values[1]
    value = values[2]
    expires_at = None
    
    if len(values) > 3:
        option = values[3].upper()
        if option == b"PX":
            milliseconds = int(values[4])
            expires_at = time.time() + (milliseconds/1000)
            hashmap[key] = (value, expires_at)
    else:
        hashmap[key] = (value, expires_at)
    return encode_as_simple_string(b"OK")

def handle_get_command(values):
    key = values[1]
    returned_value, expires_at = hashmap[key]
    if not returned_value:
        return NULL_BULK_STRING
    elif expires_at and expires_at < time.time():
        return NULL_BULK_STRING
    else:
        return encode_as_bulk_string(returned_value)