import sys
import os
import rdt3 as rdt


if __name__ == "__main__":
    MSG_LEN = rdt.PAYLOAD

    if len(sys.argv) != 4:
        print("Usage:  " + sys.argv[0] +
              "  <client IP>  <drop rate>  <error rate>")
        sys.exit(0)

    try:
        os.stat("./Store")
    except OSError as emsg:
        print("Directory './Store' does not exist!!")
        print("Please create the directory before starting up the server")
        sys.exit(0)

    rdt.rdt_network_init(sys.argv[2], sys.argv[3])

    rdtSocket = rdt.rdt_socket()
    if rdtSocket == None:
        sys.exit(0)

    if rdt.rdt_bind(rdtSocket, rdt.SPORT) == -1:
        sys.exit(0)

    if rdt.rdt_peer(sys.argv[1], rdt.CPORT) == -1:
        sys.exit(0)

    receivedMessage = rdt.rdt_recv(rdtSocket, MSG_LEN)
    if receivedMessage == b'':
        sys.exit(0)
    else:
        filelength = int(receivedMessage)
        print("Received client request: file size =", filelength)
    receivedMessage = rdt.rdt_recv(rdtSocket, MSG_LEN)
    if receivedMessage == b'':
        sys.exit(0)
    else:
        filename = "./Store/" + receivedMessage.decode("ascii")
        try:
            fileObject = open(filename, 'wb')
        except OSError as emsg:
            print("Encountered file error: ", emsg)
        if fileObject:
            print("Open file", filename, "for writing successfully")
            osize = rdt.rdt_send(rdtSocket, b'OKAY')
            if osize < 0:
                print("Unable to respond to the message")
                sys.exit(0)
        else:
            print("Unable to open file", filename, "for writing")
            osize = rdt.rdt_send(rdtSocket, b'ERROR')
            sys.exit(0)

    print("Start receiving the file . . .")
    received = 0
    while received < filelength:
        print("---- Server progress: %d / %d" % (received, filelength))
        receivedMessage = rdt.rdt_recv(rdtSocket, MSG_LEN)
        if receivedMessage == b'':
            print("Encountered receive error! Has received", received, "so far.")
            sys.exit(0)
        else:
            wsize = fileObject.write(receivedMessage)
            received += wsize

    fileObject.close()
    rdt.rdt_close(rdtSocket)
    print("File Transfer Complete!")
