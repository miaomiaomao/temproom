# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 18:41:35 2017

@author: Lenovo
"""

import pymysql
import pandas as pd
import datetime
import random
 
conn=pymysql.connect(host='localhost',user='root',passwd='960115',db='temproomdata',port=3306)
cur=conn.cursor()

#%%判断是否新用户
while(1):
    decision = input('是否选择注册新用户，请输入y/n:')
    if decision != 'y' and decision != 'n':
        print('输入无效，请重新输入！')
    else:
        break

#新用户注册
if decision=='y':
    while(1):
        username = input('请输入用户名:')
        if len(username)>30:
            print('用户名过长，请重新输入！')
            continue
        sql = "select * from users where username = '" + username + "'"
        cur.execute(sql)
        if cur.rowcount!=0:
            print('该用户名已被注册！')
            continue
        break
    while(1):
        password = input('请输入密码(区分大小写)：')
        if len(password)>30:
            print('密码过长，请重新输入！')
            continue
        break
    sex = input('请勾选性别：')
    
    while(1):
        nickname = input('请输入昵称：')
        if len(password)>30:
            print('昵称过长，请重新输入！')
            continue
        break
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = """insert into users
	values('%s','%s','%s','%s','%s',%d)"""
    cur.execute(sql % (username,password,sex,nickname,today,0))
    conn.commit()

#老用户登陆
if decision=='n':
    while(1):
        username = input('请输入用户名：')
        sql = "select * from users where username = '" + username + "'"
        cur.execute(sql)
        if cur.rowcount==0:
            print('该用户不存在！')
            continue
        data = pd.DataFrame(list(cur.fetchall()))
        cursor_des = pd.DataFrame(list(cur.description))
        data.columns = list(cursor_des[0])
        break
    
    while(1):
        password = input('请输入密码：')
        if password != data['password'][0]:
            print('密码错误！')
            continue
        break

#%%判断创建新房间还是进入已有房间
#创建房间
while(1):
    roomnumber = str(random.randint(1000, 9999))
    sql = "select * from rooms where roomnumber = " + roomnumber
    cur.execute(sql)
    if cur.rowcount!=0:
        continue
    
    sql = """insert into rooms
	values(%d,%d)"""
    cur.execute(sql % (int(roomnumber),1))
    conn.commit()
    
    sql = """update users
	set currentroom = %d
	where username='%s'"""
    cur.execute(sql % (int(roomnumber),username))
    conn.commit()
    break

#进入已有房间
while(1):
    roomnumber = input('请输入房间号：')
    sql = "select * from rooms where roomnumber = " + roomnumber
    cur.execute(sql)
    if cur.rowcount==0:
        print('该房间不存在！请重新确认房间号码。')
        continue
    print('进入房间成功！')
    
    sql = """update rooms
	set numberofusers = numberofusers+1
	where roomnumber = %d"""
    cur.execute(sql % (int(roomnumber)))
    conn.commit()
    
    sql = """update users
	set currentroom = %d
	where username='%s'"""
    cur.execute(sql % (int(roomnumber),username))
    conn.commit()
    break
#%%退出房间
sql = """update rooms
	set numberofusers = numberofusers-1
	where roomnumber = %d"""
cur.execute(sql % (int(roomnumber)))
conn.commit()

sql = """update users
	set currentroom = %d
	where username='%s'"""
cur.execute(sql % (0,username))
conn.commit()



#username = 'han'

'''
sql = """delete from users
	where username='id'"""
cur.execute(sql)
conn.commit()
'''