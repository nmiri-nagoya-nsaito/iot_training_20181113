# -*- coding: utf-8 -*-
import time
import picamera
import io
import tornado
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
from threading import Thread
import os

WIDTH = 360
HEIGHT = 270
FPS = 30

# HTTP接続時に処理するハンドラ
class HttpHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    # GETメソッドの処理
    # HTTPアクセスを受け付けたらcamera.htmlを返す
    # index.html にはWebSocket接続を確立させるスクリプトが入っている
    def get(self):
        self.render("camera.html",
                   host_addr = self.get_ip(),
                   )

    # 自ホストのIPアドレスを取得
    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        return ip

# WebSocket接続時に処理するハンドラ
class WSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, camera):
        self.camera = camera
        self.state = True

    def open(self):
        print(self.request.remote_ip, ": connection opened")
        t = Thread(target=self.loop)

        # デーモンに設定する
        t.setDaemon(True)
        t.start()

    def loop(self):
        stream = io.BytesIO()

        for foo in self.camera.capture_continuous(stream, "jpeg"):
            stream.seek(0)
            self.write_message(stream.read(), binary=True)
            stream.seek(0)
            stream.truncate()
            if not self.state:
                break

    def on_close(self):
        self.state = False     #映像送信のループを終了させる
        self.close()     #WebSocketセッションを閉じる
        print(self.request.remote_ip, ": connection closed")

def get_camera():
    camera = picamera.PiCamera()
    camera.resolution = (WIDTH, HEIGHT)
    camera.framerate = FPS
    #camera.start_preview()
    camera.start_preview(fullscreen=False, window=(100,20,320,240))
    
    time.sleep(2)        #カメラ初期化
    return camera

# メイン処理
def main():
    camera = get_camera()
    print("camera initialized.")
    
    # Webアプリの起動
    app = tornado.web.Application([
        (r"/", HttpHandler),                           # HTTP接続
        (r"/camera", WSHandler, dict(camera=camera)),  # WebSocket接続
    ],
    template_path=os.path.join(os.getcwd(), "template"),
    static_path=os.path.join(os.getcwd(), "static"),
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

# 定義は以上．ここからプログラム開始

if __name__ == "__main__":
    main()