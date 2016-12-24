from flask import Flask
import subprocess
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

color = {}
color["\n"] = "<br>"
color["[0m"] = "</font>"
color["[36m"] = "<font color='blue'>"
color["[32m"] = "<font color='green'>"
color["[33m"] = "<font color='gold'>"
color["[35m"] = "<font color='orange'>"
color["[31m"] = "<font color='red'>"

@app.route("/")
def root():
	proc = subprocess.Popen(["python2", dir_path + "/predict.py"], stdout=subprocess.PIPE)
	(out, err) = proc.communicate()
	for i in color:
		out = out.replace(i,color[i])
	return out, 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)
