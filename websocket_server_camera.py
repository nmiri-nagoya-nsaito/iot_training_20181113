# -*- coding: utf-8 -*-
import json
import time

import random

import tornado.websocket
import tornado.web
import tornado.ioloop

import picamera

class HttpHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    # GETメソッドの処理
    # HTTPアクセスを受け付けたらindex.htmlを返す
    # index.html にはWebSocket接続を確立させるスクリプトが入っている
    def get(self):
        self.render("./client.html")  

class CamWebSocket(tornado.websocket.WebSocketHandler):
    def initialize(self, camera):
        self.camera = camera
        self.state = True

    def open(self):
        print ('Cam: Session Opened. IP:' + self.request.remote_ip)
        self.ioloop = tornado.ioloop.IOLoop.instance()

        t = Thread(target=self.send_websocket)
        t.setDaemon(True)
        t.start()

    def on_close(self):
        print("Cam: Session closed")
        self.state = False     #映像送信のループを終了させる
        self.close()     #WebSocketセッションを閉じる

    def check_origin(self, origin):
        return True

    def send_websocket(self):
        for foo in self.camera.capture_continuous(stream, "jpeg"):
            stream.seek(0)
            self.write_message(stream.read(), binary=True)
            stream.seek(0)
            stream.truncate()
            if not self.state:
                break 

#        self.ioloop.add_timeout(time.time() + 0.1, self.send_websocket)
#            message = json.dumps({
#            'data1': random.randint(0, 100),
#            'data2': random.randint(0, 100),
#            })
#        self.write_message(message)


class SendWebSocket(tornado.websocket.WebSocketHandler):
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
            message = json.dumps({
                'data1': random.randint(0, 100),
                'data2': random.randint(0, 100),
                })
            self.write_message(message)

# 処理開始
camera = picamera.PiCamera()
camera.resolution = (WIDTH, HEIGHT)
camera.framerate = FPS
camera.start_preview()

time.sleep(2)        #カメラ初期化



app = tornado.web.Application([
    (r"/", HttpHandler),
    (r"/ws/display", SendWebSocket),
    (r"/camera", CamWebSocket, dict(camera=camera)),
])

if __name__ == "__main__":
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()