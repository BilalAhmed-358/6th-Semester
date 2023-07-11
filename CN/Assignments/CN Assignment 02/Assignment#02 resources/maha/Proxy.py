from socket import *
import signal
from urllib.request import Request, urlopen, HTTPError
from _thread import *
import os


def check_blocklist(fname):
    fh = open('filterSites.txt', 'r')
    fsite = fh.read()
    sites = fsite.split('\n')
    fh.close()
    if fname in sites:
        return True
    else:
        return False


def fetch_cache(site):
    global urls
    try:
        fh = open('cache'+site, encoding="ISO-8859-1")
    except IOError:
        print("File not found")
        return None
    content = fh.read()
    fh.close
    if site.count('/') == 1:
        url = 'http://www.' + site[1:]
        urls = url
    else:
        url = 'http://www.' + site
        urls = url
    return content


def save_in_cache(filename, content):
    print('Saving a copy of {} in the cache'.format(filename))
    print(filename)
    filename = filename.split('?')[0]
    print(filename)
    print(filename)
    cached_file = open('cache' + filename, 'w', encoding="ISO-8859-1")
    cached_file.write(content)
    cached_file.close()


def fetch_file(site):
    file_cache = fetch_cache(site)
    if file_cache is not None:
        return file_cache
    else:
        global urls
        if site.count('/') == 1:
            url = 'http://www.' + site[1:]
            urls = url
        else:
            url = urls+site
            print(urls)

        print("url here", url)
        # try:
        q = Request(url)
        response = urlopen(q)
        response_headers = response.info()
        content = response.read().decode("ISO-8859-1")
        save_in_cache(site, content)
        return content
        # except HTTPError:
        #     print('error')
        #     return None


if __name__ == "__main__":
    urls = ''
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    tcpServerPort = int(input("Enter port number: "))
    tcpServerSocket = socket(AF_INET, SOCK_STREAM)

    tcpServerSocket.bind(('127.0.0.1', tcpServerPort))
    tcpServerSocket.listen(100)

    buffer_size = 4096

    while True:
        print("Server is listening")
        tcpClientSocket, address = tcpServerSocket.accept()

        print("Recevied a connection from: ", address)
        message = tcpClientSocket.recv(buffer_size).decode()
        print(message)
        print(message.split()[1])
        site = message.split()[1]
        print(site)

        if check_blocklist(site[1:]) == True:
            site = '/block.html'

        # Get the file
        content = fetch_file(site)

        # If we have the file, return it, otherwise 404
        if content:
            response = 'HTTP/1.0 200 OK\n\n' + content
        else:
            response = 'HTTP/1.0 404 NOT FOUND\n\n File Not Found'

        tcpClientSocket.sendall(response.encode())
        tcpClientSocket.close()
