import socket
import random
import struct
import select

PAYLOAD = 1000
CPORT = 1234
SPORT = 2000
TIMEOUT = 0.05
TWAIT = 10 * TIMEOUT
TYPE_DATA = 12
TYPE_ACK = 11
MSG_FORMAT = 'B?HH'
HEADER_SIZE = 6


__peeraddr = ()
__LOSS_RATE = 0.0
__ERR_RATE = 0.0
__data_buffer = []
__send_seq_num = 0
__recv_seq_num = 0
__last_ack_no = None


def __udt_send(socketId, peerAddress, byteMessage):
    global __LOSS_RATE, __ERR_RATE
    if peerAddress == ():
        print("Socket send error: Peer address not set yet")
        return -1
    else:
        drop = random.random()
        if drop < __LOSS_RATE:
            print("WARNING: udt_send: Packet lost in unreliable layer!!")
            return len(byteMessage)

        corrupt = random.random()
        if corrupt < __ERR_RATE:
            err_bytearr = bytearray(byteMessage)
            pos = random.randint(0, len(byteMessage) - 1)
            val = err_bytearr[pos]
            if val > 1:
                err_bytearr[pos] -= 2
            else:
                err_bytearr[pos] = 254
            err_msg = bytes(err_bytearr)
            print("WARNING: udt_send: Packet corrupted in unreliable layer!!")
            return socketId.sendto(err_msg, peerAddress)
        else:
            return socketId.sendto(byteMessage, peerAddress)


def __udt_recv(socketId, length):
    (rmsg, peer) = socketId.recvfrom(length)
    return rmsg


def __int_chksum(byteMessage):
    total = 0
    length = len(byteMessage)
    i = 0
    while length > 1:
        total += ((byteMessage[i + 1] << 8) & 0xFF00) + ((byteMessage[i]) & 0xFF)
        i += 2
        length -= 2

    if length > 0:
        total += (byteMessage[i] & 0xFF)

    while (total >> 16) > 0:
        total = (total & 0xFFFF) + (total >> 16)

    total = ~total
    return total & 0xFFFF


def rdt_network_init(drop_rate, err_rate):
    random.seed()
    global __LOSS_RATE, __ERR_RATE
    __LOSS_RATE = float(drop_rate)
    __ERR_RATE = float(err_rate)
    print("Drop rate:", __LOSS_RATE, "\tError rate:", __ERR_RATE)


def rdt_socket():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as err_msg:
        print("Socket creation error: ", err_msg)
        return None
    return sock


def rdt_bind(socketId, port):
    try:
        socketId.bind(("", port))
    except socket.error as err_msg:
        print("Socket bind error: ", err_msg)
        return -1
    return 0


def rdt_peer(peer_ip, port):
    global __peeraddr
    __peeraddr = (peer_ip, port)


def __make_data(seq_num, data):
    global TYPE_DATA, MSG_FORMAT
    msg_format = struct.Struct(MSG_FORMAT)
    checksum = 0
    init_msg = msg_format.pack(
        TYPE_DATA, seq_num, checksum, socket.htons(len(data))) + data

    checksum = __int_chksum(bytearray(init_msg))
    complete_msg = msg_format.pack(
        TYPE_DATA, seq_num, checksum, socket.htons(len(data))) + data
    return complete_msg


def __unpack_helper(msg):
    global MSG_FORMAT
    size = struct.calcsize(MSG_FORMAT)
    (msg_type, seq_num, recv_checksum, payload_len), payload = struct.unpack(
        MSG_FORMAT, msg[:size]), msg[size:]
    return (msg_type, seq_num, recv_checksum, socket.ntohs(payload_len)), payload


def __is_corrupt(recv_pkt):
    global MSG_FORMAT
    (msg_type, seq_num, recv_checksum,
     payload_len), payload = __unpack_helper(recv_pkt)
    init_msg = struct.Struct(MSG_FORMAT).pack(
        msg_type, seq_num, 0, socket.htons(payload_len)) + payload

    calc_checksum = __int_chksum(bytearray(init_msg))
    result = recv_checksum != calc_checksum
    return result


def __is_ack(recv_pkt, seq_num):
    global TYPE_ACK
    (msg_type, recv_seq_num, _, _), _ = __unpack_helper(recv_pkt)
    return msg_type == TYPE_ACK and recv_seq_num == seq_num


def __has_seq(recv_msg, seq_num):
    (msg_type, recv_seq_num, _, _), _ = __unpack_helper(recv_msg)
    return recv_seq_num == seq_num


def __cut_msg(byteMessage):
    global PAYLOAD
    if len(byteMessage) > PAYLOAD:
        msg = byteMessage[0:PAYLOAD]
    else:
        msg = byteMessage
    return msg


def rdt_send(socketId, byteMessage):
    global PAYLOAD, __peeraddr, __data_buffer, HEADER_SIZE, __send_seq_num, __last_ack_no
    msg = __cut_msg(byteMessage)
    snd_pkt = __make_data(__send_seq_num, msg)
    try:
        sent_len = __udt_send(socketId, __peeraddr, snd_pkt)
    except socket.error as err_msg:
        print("Socket send error: ", err_msg)
        return -1
    print("rdt_send(): Sent one message [%d] of size %d --> " % (__send_seq_num, sent_len)
          + str(__unpack_helper(snd_pkt)[0]))

    r_sock_list = [socketId]
    recv_expected = False
    while not recv_expected:
        r, _, _ = select.select(r_sock_list, [], [], TIMEOUT)
        if r:
            for sock in r:
                try:
                    recv_msg = __udt_recv(sock, PAYLOAD + HEADER_SIZE)
                except socket.error as err_msg:
                    print("__udt_recv error: ", err_msg)
                    return -1
                if __is_corrupt(recv_msg) or __is_ack(recv_msg, 1 - __send_seq_num):
                    print("rdt_send(): recv [corrupt] OR unexpected [ACK %d] | Keep waiting for ACK [%d]"
                          % (1-__send_seq_num, __send_seq_num))
                elif __is_ack(recv_msg, __send_seq_num):
                    print(
                        "rdt_send(): Received expected ACK [%d]!" % __send_seq_num)
                    __send_seq_num ^= 1
                    return sent_len - HEADER_SIZE
                else:
                    print("rdt_send(): recv DATA ?! -buffer-> " +
                          str(__unpack_helper(recv_msg)[0]))
                    if recv_msg not in __data_buffer:
                        __data_buffer.append(recv_msg)
                    (_, data_seq_num, _, _), _ = __unpack_helper(recv_msg)
                    try:
                        __udt_send(socketId, __peeraddr, __make_ack(data_seq_num))
                    except socket.error as err_msg:
                        print(
                            "rdt_send(): Error in sending ACK to received data: " + str(err_msg))
                        return -1

                    __last_ack_no = data_seq_num
                    print("rdt_send(): ACK DATA [%d]" % data_seq_num)
        else:
            print("! PACKET TIMEOUT !")

            try:
                sent_len = __udt_send(socketId, __peeraddr, snd_pkt)
            except socket.error as err_msg:
                print("Socket send error: ", err_msg)
                return -1
            (_), payload = __unpack_helper(snd_pkt)
            print("rdt_send(): Re-sent one message [%d] of size %d -> " % (__send_seq_num, sent_len)
                  + str(__unpack_helper(snd_pkt)[0]))


def __make_ack(seq_num):
    global TYPE_ACK, MSG_FORMAT
    msg_format = struct.Struct(MSG_FORMAT)
    checksum = 0
    init_msg = msg_format.pack(
        TYPE_ACK, seq_num, checksum, socket.htons(0)) + b''
    checksum = __int_chksum(bytearray(init_msg))
    return msg_format.pack(TYPE_ACK, seq_num, checksum, socket.htons(0)) + b''


def rdt_recv(socketId, length):
    global __peeraddr, __data_buffer, __recv_seq_num, HEADER_SIZE, __last_ack_no
    while len(__data_buffer) > 0:
        recv_pkt = __data_buffer.pop(0)
        print("rdt_recv(): <!> Something in buffer! -> " +
              str(__unpack_helper(recv_pkt)[0]))
        if __has_seq(recv_pkt, __recv_seq_num):
            print("rdt_recv(): Received expected buffer DATA [%d] of size %d" % (
                __recv_seq_num, len(recv_pkt)))
            __recv_seq_num ^= 1
            return __unpack_helper(recv_pkt)[1]

    recv_expected_data = False
    while not recv_expected_data:
        try:
            recv_pkt = __udt_recv(socketId, length + HEADER_SIZE)
        except socket.error as err_msg:
            print("rdt_recv(): Socket receive error: " + str(err_msg))
            return b''
        if __is_corrupt(recv_pkt) or __has_seq(recv_pkt, 1-__recv_seq_num):
            print("rdt_recv(): Received [corrupted] or [wrong seq_num (%d)] -> " % (1-__recv_seq_num)
                  + str(__unpack_helper(recv_pkt)[0]) + "Keep expecting seq [%d]" % __recv_seq_num)
            print("----corrupt? => " + str(__is_corrupt(recv_pkt)))
            snd_ack = __make_ack(1-__recv_seq_num)
            try:
                __udt_send(socketId, __peeraddr, snd_ack)
            except socket.error as err_msg:
                print(
                    "rdt_recv(): Error in ACK-ing corrupt/wrong data packet: " + str(err_msg))
                return b''
            __last_ack_no = 1-__recv_seq_num
            print("rdt_recv(): Sent old ACK [%d]" % (1-__recv_seq_num))
        elif __has_seq(recv_pkt, __recv_seq_num):
            (_), payload = __unpack_helper(recv_pkt)
            print(("rdt_recv(): Received expected DATA [%d] of size %d" % (
                __recv_seq_num, len(recv_pkt))))

            try:
                __udt_send(socketId, __peeraddr, __make_ack(__recv_seq_num))
            except socket.error as err_msg:
                print("rdt_recv(): Error in ACK-ing expected data: " + str(err_msg))
                return b''
            print("rdt_recv(): Sent expected ACK [%d]" % __recv_seq_num)
            __last_ack_no = __recv_seq_num
            __recv_seq_num ^= 1
            return payload


def __is_data(recv_pkt, seq_num):
    global TYPE_DATA
    (pkt_type, pkt_seq, _, _), _ = __unpack_helper(recv_pkt)
    return pkt_type == TYPE_DATA and pkt_seq == seq_num


def rdt_close(socketId):
    global __last_ack_no
    r_sock_list = [socketId]
    ok_to_close = False

    while not ok_to_close:
        r, _, _ = select.select(r_sock_list, [], [],
                                TWAIT)
        if r:
            for sock in r:
                try:
                    recv_pkt = __udt_recv(
                        sock, PAYLOAD + HEADER_SIZE)
                except socket.error as err_msg:
                    print("rdt_close(): __udt_recv error: ", err_msg)
                print("rdt_close(): Got activity -> " +
                      str(__unpack_helper(recv_pkt)[0]))
                if not __is_corrupt(recv_pkt) and __is_data(recv_pkt, __last_ack_no):
                    try:
                        __udt_send(socketId, __peeraddr,
                                   __make_ack(__last_ack_no))
                    except socket.error as err_msg:
                        print("rdt_close(): Error in ACK-ing data: " + str(err_msg))
                    print("rdt_close(): Sent last ACK[%d]" % __recv_seq_num)
        else:
            print("rdt_close(): time to CLOSE!!!")
            ok_to_close = True
            try:
                socketId.close()
            except socket.error as err_msg:
                print("Socket close error: ", err_msg)
