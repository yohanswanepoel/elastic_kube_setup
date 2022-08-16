from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sys
import platform
#import config
import re
import utils
from forms import ConfigForm, InstallOperatorForm, DeployStackForm
from flask_bootstrap import Bootstrap


# to run 
# export FLASK_APP=app
# export FLASK_ENV=development

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
bootstrap = Bootstrap(app)

config = utils.get_config()

@app.route('/')
def index():
    global config
    errors = []
    if utils.cluster_running():
        spaces = utils.get_namespaces()
    else:
        errors.append("Cluster may not be running or cluster type incorrect. Please configure k8s")
        spaces = []
    return render_template('index.html', namespaces = spaces, errors=errors)

@app.route("/install_operator", methods=('GET', 'POST'))
def install_operator():
    global config
    errors = []
    form = InstallOperatorForm()
    form.operator_version.choices = [(c, c) for c in config["operator_versions"]]
    if form.validate_on_submit():
        flash("Installing Operator")
        flash(utils.install_operator(form.operator_version.data))
    return render_template("install_operator.html", form=form, errors=errors)

@app.route('/deploy', methods=('GET', 'POST'))
def deploy():
    global config
    form = DeployStackForm()
    errors = []
    form.version.choices = [(c, c) for c in config["versions"]]
    if form.validate_on_submit():
        namespace = form.namespace.data
        version = form.version.data 
        spaces = utils.get_namespaces()
        target_namespace = "eck"+"-" + namespace.strip()
        flash("Target Namespace: " + target_namespace)
        if target_namespace in spaces:
            if utils.check_elastic_exists(namespace):
                errors.append("Namespace already contains Elastic")
            else:
                flash("Deploying Elastic")
                utils.deploy_full_stack(target_namespace, namespace, version)
        else:
            flash("Creating namespace")
            utils.create_namespace(target_namespace)
            flash("Deploying Elastic")
            utils.deploy_full_stack(target_namespace, namespace, version)
    return render_template('deploy.html', form=form, errors=errors)

# kubectl get elastic
# use name that is unique - then can filter easily 
# namespace should be elk-name
# Group elastic output and namespace output together on one page
# kubectl describe elasticsearch elasticsearch-sample | grep -i namespace

@app.route('/remove_stack/<string:namespace>')
def remove_stack(namespace):
    global config
    result = utils.remove_stack(namespace)
    return redirect(url_for("namespace", namespace = namespace))

@app.route('/namespace/<string:namespace>')
def namespace(namespace):
    global config
    pods = utils.get_pods(namespace)
    services = utils.get_services(namespace)
    password = ""
    version = ""
    if utils.get_elastic_version(namespace) != "":
        password = utils.get_elastic_password(namespace)
        version = utils.get_elastic_version(namespace)
    return render_template("namespace.html", pods = pods, services=services,  namespace = namespace, version=version, password = password)

@app.route('/delete_namespace/<string:namespace>')
def delete_namespace(namespace):
    global config
    utils.remove_namespace(namespace)
    return redirect(url_for("index"))

@app.route('/set_config', methods=('GET', 'POST'))
def set_config():
    global config
    form = ConfigForm()
    form.kubectl_command.choices = [(c, c) for c in config["kubectl_list"]]
    form.local_cluster.choices = [(c, c) for c in config["cluster_types"]]
    if form.validate_on_submit():
        config["kubectl_command"] = form.kubectl_command.data
        config["local_cluster"] = form.local_cluster.data
        utils.save_config(config)
        flash("Config Saved")
    form.kubectl_command.data = config["kubectl_command"]
    form.local_cluster.data = config["local_cluster"]
    
    return render_template("set_config.html", form=form)