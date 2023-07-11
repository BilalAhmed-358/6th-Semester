from socket import *
import sys

Server_Socket = socket(AF_INET, SOCK_STREAM)
Server_Socket.bind(('localhost', 1234))
Server_Socket.listen(3)

def Check_Block_sites(msg):
    print(msg.split()[1])

    file1 = str(msg, encoding='utf8')
    filename = file1.split()[1].split("/")[1]
    print("FileName:", filename)

    blockFile = open("blockSites.txt", "r")
    flag = 0
    index = 0

    for line in blockFile:
        index += 1

        if filename in line:
            flag = 1
            break

    if flag == 0:
        print('URL', filename, 'NOT PRESENT IN BLOCK SITES')
    else:
        filename = 'index.html'
    blockFile.close()
    return filename

while 1:

    print('Server is Active!!')
    Client_Socket, addr = Server_Socket.accept()
    print('Connection Received from:', addr)
    msg = Client_Socket.recv(2048)
    if str(msg, encoding='utf8') != '':

        filename = Check_Block_sites(msg)

        fileExist = "false"
        filetouse = "/" + filename
        print(filetouse)
        try:
            f = open(filetouse[1:], "rb")
            outputdata = f.readlines()
            fileExist = "true"

            Client_Socket.send(bytes("HTTP/1.0 200 OK\r\n", 'utf-8'))
            Client_Socket.send(bytes("Content-Type:text/html\r\n", 'utf-8'))

            for i in range(0, len(outputdata)):
                Client_Socket.send(outputdata[i])

            f.close()
            print('--------------------Read from cache----------------')

        except IOError:
            if fileExist == "false":

                c = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                print("HOSTNAME:", hostn)
                try:
                    c.connect((hostn, 80))
                    print('Socket is connected to port # 80')

                    fileobj = c.makefile('rwb')
                    string1 = "GET " + "http://" + filename + " HTTP/1.0\n\n"
                    naming = bytes(string1, 'utf-8')
                    c.send(naming)
                    fileobj.write(naming)

                    buff = fileobj.readlines()

                    tmpFile = open("./" + filename, "wb")
                    for i in range(0, len(buff)):
                        tmpFile.write(buff[i])
                        Client_Socket.send(buff[i])

                    tmpFile.close()
                except:
                    print("")
                else:

                    print("------------File does not exist-----------")

    Client_Socket.close()

Server_Socket.close()