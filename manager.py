# coding:utf-8
import os
import time
import hashlib
import subprocess
import threading
import signal
import logging

import tornado
# import schedule

from Config import config
import Server.server as server

########################################################

main_logger = logging.getLogger(__name__)
log_handler = logging.FileHandler('Log/main.log')
main_logger.addHandler(log_handler)

ss_log = open("Log/shadowsocks.log","a")

server_log_handler = logging.FileHandler("Log/server.log")

########################################################

def getTodayPassword():
    today = time.strftime("%a%b%d%Y", time.localtime())
    todayHash = hashlib.md5(today.encode('utf-8')).hexdigest() + config.secretKey
    todayPassword = hashlib.md5(todayHash.encode("utf-8")).hexdigest()
    return todayPassword

########################################################

def run_ss():
    cmd = "./shadowsocks-server -m chacha20-ietf -p 8888 -k "+ getTodayPassword()
    # cmd = "ping -n 100 8.8.8.8" # CMD for TEST
    main_logger.debug(cmd)
    process = subprocess.Popen(["ping", "-t",  "8.8.8.8"], stdout=ss_log) # CMD for test
    # process = subprocess.Popen(["./shadowsocks-server", "-m",  "chacha20-ietf", "-p", "8888", "-k", getTodayPassword()], stdout=ss_log)
    def signal_exit(signum, frame):  
        main_logger.info('Get Signum:', signum)
        main_logger.debug('Subprocess Pid:', process.pid)
        process.kill()
        ss_log.close()
        server_log.close()
        exit()
    signal.signal(signal.SIGTERM, signal_exit)
    signal.signal(signal.SIGINT, signal_exit)
    return process

########################################################

def run_server():
    application = tornado.web.Application([
        (r"/", server.MainHandler),
        (r"/hash/.*", server.ShareHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "Server/static"}),
    ])

    access_log = logging.getLogger("tornado.access")
    app_log = logging.getLogger("tornado.application")
    gen_log = logging.getLogger("tornado.general")
    
    tornado.log.enable_pretty_logging() 
    
    access_log.addHandler(server_log_handler)
    app_log.addHandler(server_log_handler)
    gen_log.addHandler(server_log_handler)

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()

########################################################

def main():
    server_thread = threading.Thread(target=run_server,args=())
    server_thread.setDaemon(True)
    server_thread.start()
    child_process = run_ss()
    # schedule.every().day.at("00:00").do(run_ss)
    while True:
        # schedule.run_pending()
        time.sleep(24*60*60-10)
        child_process.kill()
        time.sleep(5)
        child_process = run_ss()
        time.sleep(5)

if __name__ == '__main__':
    main()

