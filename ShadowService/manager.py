# coding:utf-8
import os
import time
import hashlib
import subprocess
import threading
import signal
import logging
import tornado
import tornado.ioloop
import tornado.iostream
import socket

# import schedule

import config

date = time.localtime().tm_mday

########################################################

main_logger = logging.getLogger(__name__)
log_handler = logging.FileHandler('Log/main.log')
main_logger.addHandler(log_handler)

ss_log = open("Log/shadowsocks.log","a")

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
    # process = subprocess.Popen(["ping", "-t",  "8.8.8.8"], stdout=ss_log) # CMD for test
    process = subprocess.Popen(["./shadowsocks-server", "-m",  "chacha20-ietf", "-p", "8888", "-k", getTodayPassword()], stdout=ss_log)
    last_execute_time = time.
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

def send_request(data=None):
    if data is not None:
        print(data.encode())
    time.sleep(60)
    if date is not time.localtime().tm_mday:
        date = time.localtime().tm_mday
        child_process.kill()
        time.sleep(5)
        child_process = run_ss()
    msg = config.ipAddress + "\r\n"
    stream.write(msg.encode())
    stream.read_until(b"\r\n", send_request)

########################################################

def main():
    child_process = run_ss()
    # schedule.every().day.at("00:00").do(run_ss)
    # while True:
    #     # schedule.run_pending()
    #     time.sleep(24*60*60-10)
    #     child_process.kill()
    #     time.sleep(5)
    #     child_process = run_ss()
    #     time.sleep(5)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    stream = tornado.iostream.IOStream(s)
    stream.connect(("shadowshare.tk", 8080), send_request)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()
