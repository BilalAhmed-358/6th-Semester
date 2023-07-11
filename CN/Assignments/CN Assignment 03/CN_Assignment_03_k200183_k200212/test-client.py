import sys
import os
import time
import rdt3 as rdt


if __name__ == "__main__":
    MSG_LEN = rdt.PAYLOAD

    if len(sys.argv) != 5:
        print(
            "Usage:  " + sys.argv[0] + "  <server IP>  <nameOfFile>  <drop rate>  <error rate>")
        sys.exit(0)
    nameOfFile = sys.argv[2]
    try:
        fileObject = open(nameOfFile, 'rb')
    except OSError as emsg:
        print("Open file error: ", emsg)
        sys.exit(0)
    print("Open file successfully")

    sizeOfFile = os.path.getsize(nameOfFile)
    print("File bytes are ", sizeOfFile)

    rdt.rdt_network_init(sys.argv[3], sys.argv[4])

    rdtSocket = rdt.rdt_socket()
    if rdtSocket == None:
        sys.exit(0)

    if rdt.rdt_bind(rdtSocket, rdt.CPORT) == -1:
        sys.exit(0)

    if rdt.rdt_peer(sys.argv[1], rdt.SPORT) == -1:
        sys.exit(0)

    osize = rdt.rdt_send(rdtSocket, str(sizeOfFile).encode("ascii"))
    if osize < 0:
        print("Cannot send message1")
        sys.exit(0)
    osize = rdt.rdt_send(rdtSocket, nameOfFile.encode("ascii"))
    if osize < 0:
        print("Cannot send message2")
        sys.exit(0)
    rmsg = rdt.rdt_recv(rdtSocket, MSG_LEN)
    if rmsg == b'':
        sys.exit(0)
    elif rmsg == b'ERROR':
        print("Server experienced file creation error.\nProgram terminated.")
        sys.exit(0)
    else:
        print("Received server positive response")

    print("Start the file transfer . . .")
    starttime = time.monotonic()
    dataSent = 0
    while dataSent < sizeOfFile:
        print("---- Client progress: %d / %d" % (dataSent, sizeOfFile))
        smsg = fileObject.read(MSG_LEN)
        if smsg == b'':
            print("End of file is reached!!")
            sys.exit(0)
        osize = rdt.rdt_send(rdtSocket, smsg)
        if osize > 0:
            dataSent += osize
        else:
            print("Experienced sending error! Has dataSent",
                  dataSent, "bytes of message so far.")
            sys.exit(0)

    endtime = time.monotonic()
    print("Completed the file transfer.")
    lapsed = endtime - starttime
    print("Total elapse time: %.3f s\tThroughtput: %.2f KB/s" %
          (lapsed, sizeOfFile / lapsed / 1000.0))

    fileObject.close()
    rdt.rdt_close(rdtSocket)
    print("Client program terminated")
