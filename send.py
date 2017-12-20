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
        s.connect(('120.79.72.9', 6666))
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    print('连接服务器成功')
    return s
    #
    # print (bytes.decode(s.recv(1024)))

def send(s,username):
    # while 1:
    filepath = username+'.wav'
    if os.path.isfile(filepath):
        # 定义定义文件信息。
        fileinfo_size = os.path.getsize(filepath)
        info=str(fileinfo_size)+' '+str(username)
        # 定义文件头信息，包含文件名和文件大小
        #fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
        s.send(info.encode())

        # s.send(str(username).encode())

        print(str(fileinfo_size),str(username))

        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print ('send over...')
                break
            s.send(data)
    # s.close()


def recv(s):
    info = s.recv(1024).decode()
    sp=info.find(' ')

    username = info[sp+1:len(info)]
    filesize = int(info[0:sp])
    if filesize:
        #print('filesize is {0}'.format(buf))
        recvd_size = 0  # 定义已接收文件的大小
        # fp = open(username+'.wav', 'wb')
        fp = open('服务器接受.wav', 'wb')
        print('start receiving...')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = s.recv(1024)
                recvd_size += len(data)
            else:
                data = s.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        print('done，接受到'+username)
        fp.close()




# if __name__ == '__main__':
#     # socket_client()
