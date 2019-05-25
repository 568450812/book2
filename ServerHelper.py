from Database import *
from Sql import *
from time import sleep


class ServerHelper:
    def __init__(self):
        self.mysqlhelper = MysqlHelper()

    def get_register(self, connfd, data):  # 处理注册请求
        tmp = data.split(" ")
        name = tmp[1]
        pwd = tmp[2]
        # 查询用户名是否存在
        sql = do_query_user(name)
        r = self.mysqlhelper.do_query(sql)
        if r != None:
            connfd.send("该用户已存在".encode())
            return
        # 插入用户
        sql = do_insert_user(name, pwd)
        try:
            self.mysqlhelper.do_insert(sql)
            self.mysqlhelper.conn.commit()
            connfd.send(b"OK")
        except:
            self.mysqlhelper.conn.rollback()
            connfd.send("注册失败".encode())

    def get_login(self, connfd, data):  # 处理登录请求
        tmp = data.split(" ")
        name = tmp[1]
        pwd = tmp[2]
        # 匹配用户名和密码
        sql = do_find_user(name, pwd)
        r = self.mysqlhelper.do_query(sql)
        if r:
            connfd.send(b"OK")
        else:
            connfd.send("登录失败".encode())

    def get_query(self, connfd, temp):  # 处理查询请求
        data = temp.split(" ")
        sql = do_query_by_bookName(data[1])
        r = self.mysqlhelper.do_query(sql)
        if r:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                for i in r:
                    value = "%s %s" % (i[1], i[2])
                    connfd.send(value.encode())
                connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())

    def get_query_author(self, connfd, temp):
        data = temp.split(" ")
        sql = do_query_by_author(data[1])
        r = self.mysqlhelper.do_query(sql)
        if r:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                for i in r:
                    value = "%s %s" % (i[1], i[2])
                    connfd.send(value.encode())
                connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())

    def get_section(self, connfd, temp):  # 处理在线阅读请求
        data = temp.split(" ")
        sql = do_query_id(data[2], data[1])
        p = self.mysqlhelper.do_query(sql)
        sql = do_section(p)
        value = self.mysqlhelper.do_query(sql)
        if value:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                list01 = [i[0] for i in value]
                msg = "$".join(list01)
                connfd.send(msg.encode())
                sleep(0.1)
                connfd.send(b"##")
        else:
            connfd.send("查找失败".encode())

    def get_read(self, connfd, temp):
        data = temp.split(" ")
        msg = "%s %s"%(data[3],data[4])
        sql = do_query_id(data[2], data[1])
        r = self.mysqlhelper.do_query(sql)
        sql = do_read(msg, r[0][0])
        r = self.mysqlhelper.do_query(sql)
        print(r)
        if r:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                f = open("%s" % r[0][0],encoding="utf-8")
                while True:
                    i = f.read(1024)
                    print(i)
                    connfd.send(i.encode())
                    if len(i)< 1024:
                        break
                sleep(0.1)
                connfd.send(b"##")
                f.close()
        else:
            connfd.send("查找失败".encode())

    def get_download(self, connfd, temp):  # 处理下载请求
        data = temp.split(" ")
        sql = do_download(data[1])
        r = self.mysqlhelper.do_query(sql)
        if r:
            connfd.send(b"OK")
            data = connfd.recv(1024).decode()
            if data == "OK":
                f = open("%s" % r[0][0])
                while True:
                    i = f.read(1024)
                    if not i:
                        connfd.send(b"##")
                        break
                    connfd.send(i.encode())
                f.close()
        else:
            connfd.send("查找失败".encode())
