from flask import Flask, render_template
import os
import sys
import platform
import config
import re


# to run 
# export FLASK_APP=app
# export FLASK_ENV=development

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    namespaces = os.popen("{kubectl} get namespace".format(kubectl = config.kubectl_command)).read()
    spaces = []
    lines = namespaces.split("\n")
    for line in lines[1:]:
        spaces.append(line.split(" ")[0])
    return render_template('index.html', namespaces = spaces)

@app.route('/deploy', methods=('GET', 'POST'))
def deploy():
    return render_template('deploy.html')

@app.route('/namespace/<string:namespace>')
def namespace(namespace):
    cmd_output = os.popen("{kubectl} get pods -n {namespace}".format(kubectl = config.kubectl_command, namespace=namespace)).read()
    pods = []
    lines = cmd_output.split("\n")
    for line in lines[1:]:
        
        pod = {}
        l_normal = re.sub(' +', ' ', line)
        
        line_split = l_normal.split(" ")
        if len(line_split) > 4:
            pod["id"] = line_split[0]
            pod["containers"] = line_split[1]
            pod["state"] = line_split[2]
            pod["restarts"] = line_split[3]
            pod["age"] = line_split[4]
            pod["line"] = line
            pods.append(pod)
    return render_template("namespace.html", pods = pods)