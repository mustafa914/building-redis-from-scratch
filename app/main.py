import asyncio
from commands import handle_command
from parser import parse_data

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

async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = await asyncio.start_server(handle_connection,"localhost", 6379)

    try:
        await server_socket.serve_forever()
    finally:
        server_socket.close()
        await server_socket.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
