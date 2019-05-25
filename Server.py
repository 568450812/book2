from socket import *
from Seversetting import *
from threading import *
from ServerHelper import *
import time

class Server:
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.bind(ADDR)
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.serverhelper=ServerHelper()

    def operation(self):
        self.sockfd.listen(5)
        while True:
            connfd,addr = self.sockfd.accept()
            client = Thread(target=self.handle,args=(connfd,))
            client.setDaemon(True)
            client.start()

    def handle(self,connfd): #接收客户端请求,解析并处理的方法
        while True:
            # 接收客户端请求
            data = connfd.recv(1024).decode()
            print(data)
            if not data or data[0] == "E":
                connfd.close()
                return
            elif data[0] == "R":
                self.serverhelper.get_register(connfd,data)
            elif data[0] == "L":
                connfd.send(b"OK")
                # self.serverhelper.get_login(connfd,data)
            elif data[0] == "B":
                self.serverhelper.get_query(connfd,data)
            elif data[0] == "A":
                self.serverhelper.get_query_author(connfd,data)
            elif data[0] == "O":
                self.serverhelper.get_section(connfd,data)
            elif data[0] == "P":
                print(data)
                self.serverhelper.get_read(connfd,data)
            elif data[0] == "D":
                print(data)
                self.serverhelper.get_download(connfd,data)
