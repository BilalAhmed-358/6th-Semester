import socket as s
import threading
import sys

# Mainting a list of the current people having conversation with each other
participant_list = []


# Functionality for recieving messages

def recieve_message(client, address):
    while True:
        try:
            reply = client.recv(1024).decode()
            reply = str(address) + " : " + str(reply)
            print(reply)
            send_message(reply, sender=client)
        except:
            reply = str(address) + " : Left"
            print(reply)
            send_message(reply, sender=client)
            participant_list.remove(client)
            sys.exit(address+" Left the conversation")


# Functionality for sending messages

def send_message(msg, sender=None):
    print("delivering message : " + msg)
    for client in participant_list:
        if sender is not client:
            print("Just delivered Message")
            client.send(msg.encode())


def listen():
    while True:
        client, address = server_socket.accept()
        participant_list.append(client)
        t1 = threading.Thread(target=recieve_message, args=(client, address))
        t1.start()


try:
    portNo = int(input("Enter port number: "))
    if (portNo > 65535):
        raise ValueError(
            "The port number must be less than 65536\nExiting the program")
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.bind(('localhost', portNo))
    server_socket.listen(5)
    print('Server Up and Running')
except ValueError as ex:
    print(ex)
    sys.exit()

print("Enter 'Quit' to terminate the Server :")

main_thread = threading.Thread(target=listen)
main_thread.start()

while True:
    pass
