import socket  # noqa: F401
import select


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment the code below to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    sockets_list = [server_socket]

    readable, _ , _ = select.select(sockets_list, [], [])

    while True:
        for s in readable:
            if s is server_socket:
                connection, _ = server_socket.accept()
                sockets_list.append(connection)
            else:
                data = s.recv(1024)
                if not data:
                    sockets_list.remove(s)
                    s.close()
                else:
                    s.sendall(b"+PONG\r\n")

    

def handle_connection(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        connection.sendall(b"+PONG\r\n")
    connection.close()


if __name__ == "__main__":
    main()
