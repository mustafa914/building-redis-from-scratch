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