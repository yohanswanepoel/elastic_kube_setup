import os
import sys
import platform
import config
import re
import config

def get_namespaces():
    namespaces = os.popen("{kubectl} get namespace".format(kubectl = config.kubectl_command)).read()
    spaces = []
    lines = namespaces.split("\n")
    for line in lines[1:]:
        spaces.append(line.split(" ")[0])
    return spaces

def get_pods(namespace):
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
    return pods

def get_services(namespace):
    cmd_output = os.popen("{kubectl} get services -n {namespace}".format(kubectl = config.kubectl_command, namespace=namespace)).read()
    lines = cmd_output.split("\n")
    return lines

def create_namespace(namespace):
    # Do we need to clean up first
    output = os.popen("{kubectl} create namespace {namespace}".format(kubectl = config.kubectl_command, namespace = namespace)).read()
    return output
    

def deploy_full_stack(namespace, name, version):
    os.environ['ELASTIC'] = version
    os.environ['ECK_DEPLOYMENT_NAME'] = name
    os.environ['ECK_NAMESPACE'] = namespace
    yaml = os.popen("envsubst '$ELASTIC,$ECK_DEPLOYMENT_NAME,$ECK_NAMESPACE' < ./operator_templates/deploy_full_stack.yaml").read()
    print(yaml)
    output = os.popen("envsubst '$ELASTIC,$ECK_DEPLOYMENT_NAME,$ECK_NAMESPACE' < operator_templates/deploy_full_stack.yaml | {kubectl} apply -f - -n {namespace}".format(kubectl = config.kubectl_command, namespace = namespace)).read()
    return output

def check_elastic_exists(namespace):
    output = os.popen("{kubectl} get elastic".format(kubectl = config.kubectl_command)).read()
    return (output.strip() != "")

def remove_stack(namespace):
    output = os.popen("{kubectl} delete elastic --all".format(kubectl = config.kubectl_command))
    return output