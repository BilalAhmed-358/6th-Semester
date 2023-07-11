import socket

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 1234

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.connect((ip, port))

    string = input("Enter the string you want to send: ")

    server.send(bytes(string, 'utf-8'))

    capital = server.recv(1024)
    capital = capital.decode('utf-8')
    print("Server Response: ", capital)
