from flask import Flask, render_template, request, redirect
import os
import sys
import platform
import config
import re
import utils


# to run 
# export FLASK_APP=app
# export FLASK_ENV=development

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    spaces = utils.get_namespaces()
    return render_template('index.html', namespaces = spaces)

@app.route('/deploy', methods=('GET', 'POST'))
def deploy():
    errors = []
    messages = []
    if request.method == "POST":
        namespace = request.form["namespace"]
        if namespace.strip() == "":
            errors.append("Namespace Required")
        version = request.form["version"]
        spaces = utils.get_namespaces()
        target_namespace = "eck"+"-" + namespace.strip() + "-" + version.replace(".","")
        # check if namespace and version is unique
        for space in spaces:
            if space == target_namespace:
                # Namespace exists does it already have an elastic deployment
                if utils.check_elastic_exists(namespace):
                    print(utils.check_elastic_exists(namespace))
                    errors.append("Namespace already contains Elastic")
                else:
                    msg = utils.create_namespace(target_namespace)
                    if msg.strip != 0:
                        messages.append(msg)
        if len(errors) == 0:
            # create the deployment
            msg = utils.deploy_full_stack(target_namespace, namespace, version)
            if msg.strip != 0:
                 messages.append(msg)


    return render_template('deploy.html', versions =  config.versions, errors=errors, messages=messages)

# kubectl get elastic
# use name that is unique - then can filter easily 
# namespace should be elk-name
# Group elastic output and namespace output together on one page
# kubectl describe elasticsearch elasticsearch-sample | grep -i namespace

@app.route('/remove_stack/<string:namespace>')
def remove_stack(namespace):
    result = utils.remove_stack(namespace)
    return redirect(url("namespace", namespace = namespace))

@app.route('/namespace/<string:namespace>')
def namespace(namespace):
    pods = utils.get_pods(namespace)
    services = utils.get_services(namespace)
    return render_template("namespace.html", pods = pods, services=services,  namespace = namespace)

