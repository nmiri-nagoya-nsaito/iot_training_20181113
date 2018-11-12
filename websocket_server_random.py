# -*- coding: utf-8 -*-
import json
import time
import os
import socket
import random

import tornado.websocket
import tornado.web
import tornado.ioloop

class HttpHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    # GETメソッドの処理
    # HTTPアクセスを受け付けたらdispdata.htmlを返す
    # index.html にはWebSocket接続を確立させるスクリプトが入っている
    def get(self):
        self.render("dispdata.html", 
                    host_addr=self.get_ip(),
                    title=self.get_argument('title', 'Demo'),
                    items=items
                   )
    
    # 自ホストのIPアドレスを取得
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip

class SendWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, items):
        self.items = items

    def open(self):
        print ('Session Opened. IP:' + self.request.remote_ip)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.send_websocket()

    def on_close(self):
        print("Session closed")

    def check_origin(self, origin):
        return True

    def send_websocket(self):
        self.ioloop.add_timeout(time.time() + 0.1, self.send_websocket)
        if self.ws_connection:
            for key in list(items.keys()):
                items[key] = random.randint(0, 100)
            message = json.dumps(items)
            self.write_message(message)

items = {}
items['data1'] = 0
items['data2'] = 0
app = tornado.web.Application([
    (r"/", HttpHandler),
    (r"/ws/display", SendWebSocket, dict(items=items)),
],
    template_path=os.path.join(os.getcwd(), "template"),
    static_path=os.path.join(os.getcwd(), "static"),
)

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()