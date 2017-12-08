# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys



def client_connect():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print (msg)
        sys.exit(1)

    print (bytes.decode(s.recv(1024)))

def send(s):
    while 1:
        filepath = '1.wav'
        if os.path.isfile(filepath):
            # 定义定义文件信息。
            fileinfo_size = os.path.getsize(filepath)

            # 定义文件头信息，包含文件名和文件大小
            #fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
            s.send(str.encode(str(fileinfo_size)))
            

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print ('{0} file send over...'.format(filepath))
                    break
                s.send(data)
        s.close()
        break

def recv(s):
    buf = bytes.decode(s.recv(1024))

    filesize = int(buf)
    if buf:
        print('filesize is {0}'.format(buf))
        recvd_size = 0  # 定义已接收文件的大小
        fp = open('2.wav', 'wb')
        print('start receiving...')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = s.recv(1024)
                recvd_size += len(data)
            else:
                data = s.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()




if __name__ == '__main__':
    # socket_client()