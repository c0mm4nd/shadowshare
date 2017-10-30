import os
import sys
import time
import hashlib

import tornado.ioloop
import tornado.web

sys.path.append('../')
from Config import config

def getTodayPassword():
    today = time.strftime("%a%b%d%Y", time.localtime())
    todayHash = hashlib.md5(today.encode('utf-8')).hexdigest() + config.secretKey
    todayPassword = hashlib.md5(todayHash.encode("utf-8")).hexdigest()
    return todayPassword

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Index.html")

    def post(self):
        self.write("/hash/"+ self.getTodayPassword())


class ShareHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("**Today**, JAPAN ip is 45.76.206.122"\
        ", HONG KONG ip is 119.28.176.178, encryption is chacha20-ietf, port is 8888, password is " + \
        getTodayPassword() + ". PASSWORD WILL CHANGE EVERYDAY")

# class CaptchaHandler()

