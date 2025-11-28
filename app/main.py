import socket  # noqa: F401
import threading


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment the code below to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    while True:
        connection, _ = server_socket.accept() 
        threads = list()
        
        x = threading.Thread(target=handle_connection, args=connection)
        threads.append(x)
        x.start()

def handle_connection(connection):
    while True:
        data = connection.recv(1024)
        connection.sendall(b"+PONG\r\n")


if __name__ == "__main__":
    main()
