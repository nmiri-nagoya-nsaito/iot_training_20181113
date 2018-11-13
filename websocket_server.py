import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
 
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
 
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('connection opened...')
 
    def on_message(self, message):
        self.write_message("The server says: " + message + " back at you")
        print('received:', message)
 
    def on_close(self):
        print('connection closed...')
 
# ここから開始

application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/', MainHandler)
],
    template_path=os.path.join(os.getcwd(), "template"),
    static_path=os.path.join(os.getcwd(), "static"),
)
 
if __name__ == "__main__":
    application.listen(9090)
    tornado.ioloop.IOLoop.instance().start()
