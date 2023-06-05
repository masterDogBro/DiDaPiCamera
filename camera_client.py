# coding: utf-8

import functools
import threading
import socket
import json
import tornado


class LoginData:
    login_data = {
        "method": "login",
        "token": "NTkxMDAwMC01OTIwMDAwLHNscw=="
    }


class Config:
    # 下行代理TCP服务器监听地址
    download_proxy_addr = ('127.0.0.1', 19001)
    # 本地udp监听地址
    ffmpeg_udp_listen_addr = ('127.0.0.1', 60001)


# TCP Connection 与下行代理建立连接，可以完成对遥控指令的回应
# 以host:port为key，保证conn不重复建立
# class TCPConnection:
#     _lock = threading.Lock()
#     _connections = {}

#     def __new__(cls, host, port):
#         key = f"{host}:{port}"
#         # 额外的存在判断，提高锁利用的效率
#         if key not in cls._connections:
#             with cls._lock:
#                 if key not in cls._connections:
#                     cls._connections[key] = super(
#                         TCPConnection, cls).__new__(cls)
#                     cls._connections[key].host = host
#                     cls._connections[key].port = port
#                     cls._connections[key].connection = socket.socket(
#                         socket.AF_INET, socket.SOCK_STREAM)
#         return cls._connections[key]

#     def connect(self):
#         try:
#             with self._lock:
#                 self.connection = socket.socket(
#                     socket.AF_INET, socket.SOCK_STREAM)
#                 self.connection.connect((self.host, self.port))
#                 self.connection.settimeout(0.1)  # 设置超时时间为0.1秒
#                 # 发送hello消息
#                 data = json.dumps(LoginData.login_data).encode()
#                 self.send(data)
#                 response = self.receive(1024 * 20)
#                 # to do 漏洞：需要对回复解析，才能确定connection能否正常建立
#                 print("连接建立请求收到回复:", response.decode())
#         except socket.error as e:
#             print("Error receiving data. Trying to reconnect...", e)
#         except Exception as e:
#             # 捕获所有异常的处理代码
#             print("An error occurred", e)

#     def send(self, data):
#         if self.connection:
#             self.connection.sendall(data)

#     def send_and_rec(self, data):
#         for _ in range(3):
#             try:
#                 self.connection.sendall(data)
#                 response = self.connection.recv(1024)
#                 print("收到回复:", response.decode())
#                 return
#             except socket.timeout as e:
#                 print("超时，重新发送数据", e)
#                 self.connect()
#             except Exception as e:
#                 # 捕获所有异常的处理代码
#                 print("An error occurred", e)
#                 self.connect()
#         print("发送失败")

#     def receive(self, buffer_size):
#         if self.connection:
#             return self.connection.recv(buffer_size)

#     def close(self):
#         if self.connection:
#             with self._lock:
#                 if self.connection:
#                     self.connection.close()
#                     self.connection = None


class CameraClient:
    def __init__(self) -> None:
        self.tcpconn = TCPConnection(Config.download_proxy_addr[0], Config.download_proxy_addr[1])
        # register socket
        self.udpconn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 设置为非阻塞，还是阻塞呢？
        self.udpconn.setblocking(0)
        self.udpconn.bind(Config.ffmpeg_udp_listen_addr)

    def start(self):
        # start listening
        io_loop = tornado.ioloop.IOLoop.current()
        callback = functools.partial(self.handle_datagram, self.udpconn)
        io_loop.add_handler(self.udpconn.fileno(), callback, io_loop.READ)
        io_loop.start()

    def handle_datagram(self, udp_sock, fd, events):
        datagram, client_address = udp_sock.recvfrom(4096)
        # ts = time.time()

        print('receive datagram from %s', client_address)
        self.tcpconn.send_and_rec(datagram)


def main():
    camera_client = CameraClient()
    camera_client.start()


if __name__ == '__main__':
    main()
