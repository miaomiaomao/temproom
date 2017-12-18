# -*- coding=utf-8 -*-


"""
file: temproom_server.py
"""
import threading
import DataBaseRelated
import recv

s=recv.server_ini(1)
clients=recv.server_connect(1,s)
print(clients[0][1])
username=recv.recv(clients[0][0])
print('用户为'+username)
recv.send(clients[0][0],username)
clients[0][0].close()

