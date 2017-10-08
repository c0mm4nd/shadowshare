import time 
import hashlib
import os

SECONDS_PER_DAY = 24 * 60 * 60
LAST_UPDATE_TIME = time.time()

# def kill_ss():
# 	import subprocess,signal
# 	p = subprocess.Popen(['ps','-A'],stdout=subprocess.PIPE)
# 	out,err = p.communicate()
# 	for line in out.splitlines():
# 		if 'shadowsocks-server' in line:
# 			pid = int(line.split(None,1)[0])
# 			os.kill(pid,signal.SIGKILL)

# def start_ss(todayhash):
# 	cmd = "./shadowsocks-server -m chacha20-ietf -p 8888 -k "+ todayhash

# 	print(cmd)
# 	if os.system(cmd) == 1:
# 		open("START_SS_FAILED","w+")

# REWRITE THE KILL AND START
import subprocess

def run_ss():
	today = time.strftime("%a%b%d%Y", time.localtime()) 
	todayhash = hashlib.md5(today.encode('utf-8')).hexdigest()
	cmd = "./shadowsocks-server -m chacha20-ietf -p 8888 -k "+ todayhash
	childprocess = subprocess.Popen(cmd, shell=True)
	return childprocess

# def kill_ss(childprocess):


# def start_ss(todayhash):
# 	cmd = "./shadowsocks-server -m chacha20-ietf -p 8888 -k "+ todayhash

# 	print(cmd)
# 	if os.system(cmd) == 1:
# 		open("START_SS_FAILED","w+")

def main(first_child_process):
	while True:
		if time.time() > (LAST_UPDATE_TIME + SECONDS_PER_DAY):
			# kill_ss()
			first_child_process.kill()
			
			# today = time.strftime("%a%b%d%Y", time.localtime()) 
			# todayhash = hashlib.md5(today.encode('utf-8')).hexdigest()
			# start_ss(todayhash)
			run_ss()

		time.sleep(60*60) 

if __name__ == '__main__':
	# start_ss(todayhash)
	first_child_process = run_ss()
	main(first_child_process)