import asyncio


async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment the code below to pass the first stage
    #

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
        print(data)
        writer.write(b"+PONG\r\n")
        await writer.drain()
    writer.close()
    await writer.wait_closed()


    


if __name__ == "__main__":
    asyncio.run(main())
