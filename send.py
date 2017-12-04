# -*- coding=utf-8 -*-


"""
file: send.py
socket client
"""

import socket
import os
import sys



def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 6666))
    except socket.error as msg:
        print (msg)
        sys.exit(1)

    print (bytes.decode(s.recv(1024)))

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


if __name__ == '__main__':
    socket_client()