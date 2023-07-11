import socket
from urllib.request import Request, urlopen, HTTPError
import argparse
import os
import sys
import datetime
import os
from pathlib import Path
import time


def server_start():
    fifo_cache_scheduling()
    HOST = 'localhost'
    PORT = 8080

    MAX_REQUEST_SIZE = 4096

    def handle_request(client_socket):
        request = client_socket.recv(MAX_REQUEST_SIZE)

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(('www.example.com', 80))
        server_socket.send(request)

        response = server_socket.recv(MAX_REQUEST_SIZE)

        client_socket.send(response)

        server_socket.close()
        client_socket.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()

        pid = os.fork()
        if pid == 0:
            handle_request(client_socket)
            os._exit(0)
        else:
            client_socket.close()


def fifo_cache_scheduling():
    entries = os.listdir(
        r"C:\Users\Bilal\Desktop\Compute Networks Assignment 02\cache")

    current_time = time.ctime()

    path = Path(r"C:\Users\Bilal\Desktop\Compute Networks Assignment 02\cache")
    for entry in entries:
        filePath = Path.joinpath(path, entry)
        creation_time = os.path.getctime(filePath)
        creation_datetime = datetime.datetime.fromtimestamp(creation_time)
        current_datetime = datetime.datetime.now()
        days_since_accessed = (current_datetime - creation_datetime).days
        if days_since_accessed > 7:
            os.remove(filePath)
            print(str(filePath) + "Deleted due cache expiration.")


def LeastRecentlyUsedScheduling():
    entries = os.listdir(
        r"C:\Users\Bilal\Desktop\Compute Networks Assignment 02\cache")

    current_time = time.ctime()

    path = Path(r"C:\Users\Bilal\Desktop\Compute Networks Assignment 02\cache")
    for entry in entries:
        filePath = Path.joinpath(path, entry)
        last_accessed_time = os.path.getatime(filePath)
        creation_datetime = datetime.datetime.fromtimestamp(last_accessed_time)
        current_datetime = datetime.datetime.now()
        days_since_accessed = (current_datetime - creation_datetime).days
        if days_since_accessed > 7:
            os.remove(filePath)
            print(str(filePath) + "Deleted due cache expiration.")


def makeDirectory(directory_):
    try:
        directory_ = directory_[1:].split("/")
        temp = 'cache/'
        for i in range(len(directory_)-1):
            temp = temp+directory_[i]
            if not os.path.exists(temp):
                os.makedirs(temp)
            temp = temp + '/'
    except:
        return None


def removal(dir):
    return dir.split('?')[0]


def main():

    LeastRecentlyUsedScheduling()

    parser = argparse.ArgumentParser()
    parser.add_argument('port')
    args = parser.parse_args()

    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = int(args.port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    server_socket.listen(5)

    print('Server started at port number: %s ...' % SERVER_PORT)

    while True:
        client_connection, client_address = server_socket.accept()

        request = client_connection.recv(4096).decode()
        headers = request.split('\n')
        top_header = headers[0].split()
        method = top_header[0]
        RecvFilename = top_header[1]
        if RecvFilename == '/':
            RecvFilename = '/index.html'

        if checkInBlocklist(RecvFilename) == True:
            RecvFilename = '/block.html'
        content = fetch_file(RecvFilename)

        if content != None:
            response = 'HTTP/1.0 200 OK\n\n' + content
        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\n File Not Found'
        client_connection.sendall(response.encode())
        client_connection.close()

    server_socket.close()


def checkInBlocklist(RecvFilename):
    block_list = []

    file_ = open('block_list.txt', 'r')

    for i in file_:
        block_list.append(i.rstrip())

    if RecvFilename in block_list:
        return True


def fetch_file(RecvFilename):
    file_from_cache = fetchFileFromCache(RecvFilename)

    if file_from_cache:
        print('Fetched successfully from cache.')
        return file_from_cache
    else:
        print('Not in cache. Fetching from server.')
        fileRecvFromServer = fetchFileFromServer(RecvFilename)

        if fileRecvFromServer:
            print(RecvFilename, "adding to cache")
            saveFileInCache(RecvFilename, fileRecvFromServer)
            return fileRecvFromServer
        else:
            return None


urls = ''


def fetchFileFromCache(RecvFilename):
    global urls
    try:
        RecvFilename = removal(RecvFilename)
        fin = open('cache' + RecvFilename, encoding="ISO-8859-1")
        content = fin.read()
        fin.close()
        if RecvFilename.count('/') == 1 and ('.com' in RecvFilename or '.pk' in RecvFilename):
            url = 'http://www.' + RecvFilename[1:]
            urls = url
        return content
    except IOError:
        return None


def FlushListen(self):
    while 1:
        try:
            PacketBytes = self.__Listener.recv(1024)
        except:
            break


def fetchFileFromServer(RecvFilename):
    global urls
    if RecvFilename.count('/') == 1 and ('.com' in RecvFilename or '.pk' in RecvFilename):
        url = 'http://www.' + RecvFilename[1:]
        urls = url
    else:
        url = urls+RecvFilename
        print(urls)

    print("url here", url)

    try:
        q = Request(url)
        response = urlopen(q)
        response_headers = response.info()
        content = response.read().decode("ISO-8859-1")
        return content

    except HTTPError as err:
        print('HTTP error occured, shutting down server')
        print(f'A HTTPError was thrown: {err.code} {err.reason}')
        sys.exit()
    except ValueError:
        print("Invalid URL, restarting server")
        sys.exit()


def saveFileInCache(RecvFilename, content):
    if not os.path.exists('cache'+RecvFilename):
        makeDirectory(RecvFilename)
    print('Saving a copy of {} in the cache'.format(RecvFilename))
    RecvFilename = removal(RecvFilename)
    try:
        cached_file = open('cache' + RecvFilename, 'w', encoding="ISO-8859-1")
    except FileNotFoundError:
        print("The required file doesn't exist, shutting down server")
        sys.exit()
    except PermissionError:
        print("You don't have the required permission for the file, shutting down server")
        sys.exit()
    cached_file.write(content)
    cached_file.close()


if __name__ == '__main__':
    main()
