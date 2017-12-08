# -*- coding=utf-8 -*-


"""
file: recv.py
socket service
"""


import socket
import threading
import time
import sys
import os
from ip import getip

s = []
conn = []
addr = []
def server_ini(client_number):

    for i in range(client_number):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.append(so)

def server_connect(client_number):
    for i in range(client_number):
        try:
            s[i].bind((getip(), 6666+i))
            s[i].listen(10)
        except socket.error as msg:
            print (msg)
            sys.exit(1)

        conn[i], addr[i] = s[i].accept()
    return conn
        # t = threading.Thread(target=deal_data, args=conn[i])
        # t.start()

def send(conn):
    filepath = '1.wav'
    if os.path.isfile(filepath):
        # 定义定义文件信息。
        fileinfo_size = os.path.getsize(filepath)

        # 定义文件头信息，包含文件名和文件大小
        # fhead = struct.pack('128sl', os.path.basename(filepath),os.stat(filepath).st_size)
        conn.send(str.encode(str(fileinfo_size)))

        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filepath))
                break
            conn.send(data)
    # conn.close()





def recv(conn):
    #print ('Accept new connection from {0}'.format(addr))
    #conn.settimeout(500)
    # conn.send(str.encode('Hi, Welcome to the server!'))

#   while 1:
    #fileinfo_size = struct.calcsize('128sl')
    buf = bytes.decode(conn.recv(1024))

    filesize=int(buf)
    if buf:
        print ('filesize is {0}'.format(buf))
        recvd_size = 0  # 定义已接收文件的大小
        fp = open('2.wav', 'wb')
        print ('start receiving...')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = conn.recv(1024)
                recvd_size += len(data)
            else:
                data = conn.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
        fp.close()
        print ('end receive...,begin to transmit')
    # conn.close()



if __name__ == '__main__':
    # socket_service()