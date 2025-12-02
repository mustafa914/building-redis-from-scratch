import asyncio
import time

hashmap = {}

async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = await asyncio.start_server(handle_connection,"localhost", 6379)

    try:
        await server_socket.serve_forever()
    finally:
        server_socket.close()
        await server_socket.wait_closed()

async def handle_connection(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        values = parse_data(data)
        response = handle_command(values)
        writer.write(response)
        await writer.drain()
    writer.close()
    await writer.wait_closed()

def handle_command(values):
    command = values[0].upper()
    if command == b"ECHO":
        arg = values[1]
        return encode_as_bulk_string(arg)
    elif command == b"PING":
        return encode_as_simple_string(b"PONG")
    elif command == b"SET":
        return handle_set_command(values)
        # key = values[1]
        # value = values[2]
        # hashmap[key] = value
        # return encode_as_simple_string(b"OK")
    elif command == b"GET":
        return handle_get_command(values)
        # key = values[1]
        # returned_value = hashmap[key]
        # if not returned_value:
        #     return "$-1\r\n"
        # else:
        #     return encode_as_bulk_string(returned_value)

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
        return b"$-1\r\n"
    elif expires_at and expires_at < time.time():
        return b"$-1\r\n"
    else:
        return encode_as_bulk_string(returned_value)

    




def encode_as_bulk_string(value):
    len_string = len(value)
    bytestr_len_string = str(len_string).encode()
    bulk_string = b"$"+ bytestr_len_string + b"\r\n" + value + b"\r\n"
    return bulk_string

def encode_as_simple_string(value):
    return b"+" + value + b"\r\n"

def parse_data(data):
    return parse_resp_array(data)

def parse_resp_array(data):
    header_end = data.find(b"\r\n")
    length_array = data[1:header_end]
    count_array = int(length_array)
    parsed_strings_list = []
    remaining = data[header_end+2:]
    for i in range(count_array):
        value, remaining = parse_resp_bulk_string(remaining)
        parsed_strings_list.append(value)
    
    return parsed_strings_list


def parse_resp_bulk_string(data):
    header_end = data.find(b"\r\n")
    length_string = data[1:header_end]
    length = int(length_string)
    start = header_end + 2
    end = start + length
    value = data[start:end]
    remaining = data[end+2:]
    return value, remaining 




if __name__ == "__main__":
    asyncio.run(main())
