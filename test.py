# -*- coding=utf-8 -*-
import record
import send
import socket

record.record('123')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('120.79.72.9', 6666))
send.send(s,'123')
send.recv(s)
