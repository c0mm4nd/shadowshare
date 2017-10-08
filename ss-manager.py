import os
import time 
import hashlib
import subprocess

import schedule

import config


def getTodayPassword():
    today = time.strftime("%a%b%d%Y", time.localtime()) 
    todayHash = hashlib.md5(today.encode('utf-8')).hexdigest() + config.secretKey
    todayPassword = hashlib.md5(todayHash.encode("utf-8")).hexdigest()
    return todayPassword

def run_ss():
    cmd = "./shadowsocks-server -m chacha20-ietf -p 8888 -k "+ getTodayPassword()
    # cmd = "ping -n 100 8.8.8.8" # CMD for TEST
    print(cmd)
    childprocess = subprocess.Popen(cmd, shell=True)
    schedule.every(24).hours.do(childprocess.kill)

def main():
    first_child_process = run_ss()
    schedule.every().day.at("00:00").do(run_ss)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
