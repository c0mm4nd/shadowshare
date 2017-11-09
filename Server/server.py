#! /usr/bin/env python
# coding: utf-8

import os
import sys
import time
import hashlib
import logging

import tornado.tcpserver
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.iostream


import config

###############################################################################################


server_log_handler = logging.FileHandler("Log/server.log")

shadow_server_list = []

###############################################################################################

def getTodayPassword():
    today = time.strftime("%a%b%d%Y", time.localtime())
    todayHash = hashlib.md5(today.encode('utf-8')).hexdigest() + config.secretKey
    todayPassword = hashlib.md5(todayHash.encode("utf-8")).hexdigest()
    return todayPassword

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args):
        self.render("Index.html")

    def post(self, *args):
        self.write("/hash/"+ getTodayPassword())


class ShareHandler(tornado.web.RequestHandler):
    def get(self, *args):
        # self.write("**Today**, JAPAN ip is 45.76.206.122"\
        # ", HONG KONG ip is 119.28.176.178, encryption is chacha20-ietf, port is 8888, password is " + \
        # getTodayPassword() + ". PASSWORD WILL CHANGE EVERYDAY")
        print(len(shadow_server_list))
        if len(shadow_server_list) is 0:
            self.write("No server aviliable now. Please wait for initialization.")
        else:
            self.render("ServerList.html", ip_list=shadow_server_list, pwd=getTodayPassword())


###############################################################################################

# Steps 
# 
# 1 register a new server object
# 
# 2 keeplive through the connection
# 
# 3 if any fault occurs, deal with them (e.g. disconnection)



class ShadowsocksServerHandler(tornado.tcpserver.TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print("New connection :", address, stream)
        while True:
            try:
                data = yield stream.read_until(b"\r\n")
                msg = data.split(b"\r\n")[0]
                # if hashlib.md5(address + config.secretKey).hexdigest() == msg[0].encode():
                ip = address[0]
                print(shadow_server_list)
                if ip not in shadow_server_list:
                    shadow_server_list.append(ip)
                yield stream.write(b"RCV\r\n")
                # else:
                #     print("PASS MSG from ", address)
                #     break

            except tornado.iostream.StreamClosedError:
                print("ERROR on ", address)
                ip = address[0]
                if ip in shadow_server_list:
                    shadow_server_list.remove(ip)
                break

###############################################################################################
 
class Application(tornado.web.Application):  
    def __init__(self):  
        handlers = [
            (r"/", MainHandler),
            (r"/hash/(.*)", ShareHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "Static"})
        ]
  
        settings = { "template_path": "Templates"}  
        tornado.web.Application.__init__(self, handlers, **settings)  

###############################################################################################

def run_server():
    application = Application()

    access_log = logging.getLogger("tornado.access")
    app_log = logging.getLogger("tornado.application")
    gen_log = logging.getLogger("tornado.general")
    
    tornado.log.enable_pretty_logging() 
    
    access_log.addHandler(server_log_handler)
    app_log.addHandler(server_log_handler)
    gen_log.addHandler(server_log_handler)

    ss_receiver = ShadowsocksServerHandler()
    ss_receiver.listen(8080)
    
    server = tornado.httpserver.HTTPServer(application)
    server.listen(80)

    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    run_server()
