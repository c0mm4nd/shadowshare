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

class ShadowsocksServerHandler(tornado.tcpserver.TCPServer):
    @tornado.gen.coroutine
    def handle_stream(self, stream, address):
        print("New connection :", address, stream)
        while True:
            try:
                data = yield stream.read_until(b"\r\n")
                msg = data.split(b"\r\n")[0]
                new_server_ip = msg[0]
                yield stream.write(b"RCV")
                print(data)
            except tornado.iostream.StreamClosedError:
                break


def main():
	ss_receiver = ShadowsocksServerHandler()
	ss_receiver.listen(8080)
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()