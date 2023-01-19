import socket
import threading
import re

import win32api

from mainWindow import mainWindow
from log import Log


class http:

    @staticmethod
    def data_handle(data):
        data = data.split(";")
        if data[0] == '0':
            compile = re.compile('(.*?)maidata[.]txt')
            track_root = compile.findall(data[1])[0]
            track_root += "track.mp3"
            Log.Message(track_root)
            mainWindow.select_file(track_root)
            return
        elif data[0] == '1':
            Log.Message(data)
            mainWindow.get_data_from_edit(float(data[1]), float(data[2]), data[3], data[4], data[5], data[6])
            return

    @staticmethod
    def handle_client(client: socket.socket, address):
        # 接收客户端的请求
        data = client.recv(0x4000)
        data = data.decode('utf-8').split('\r\n')
        Log.Message(address)
        Log.Message(data)
        if data[3] == 'Expect: 100-continue':
            response = "HTTP/1.1 100 Continue\r\n"
            response += "\r\n"
            client.sendall(response.encode('utf-8'))
            data = client.recv(0x4000)
            data = data.decode('utf-8').split('\r\n')[0]
            Log.Message(data)
            response = "HTTP/1.1 200 OK\r\n"
            response += "\r\n"
            client.sendall(response.encode('utf-8'))
            client.close()
        http.data_handle(data)

    @staticmethod
    def web_start():
        try:
            with socket.socket(type=socket.SOCK_STREAM) as server:
                server.bind(("", 23333))
                server.listen(4)
                # 打印启动信息
                print("服务器已经启动！")
                # 不停的接收客户端的请求
                while True:
                    client, address = server.accept()
                    thread = threading.Thread(target=http.handle_client, args=(client, address))
                    thread.start()
        except:
            win32api.MessageBox(0, "通讯端口23333被占用,请尝试关闭对应软件", "mai_mp3", 0)
            exit(0)

