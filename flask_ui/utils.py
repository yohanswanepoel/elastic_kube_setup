import os
import sys
import platform
import config
import re
import config
import json

config = {}

def get_namespaces():
    cmd_output = os.popen("{kubectl} get namespace -o json".format(kubectl = config["kubectl_command"])).read()
    json_output = json.loads(cmd_output)
    spaces = []
    for item in json_output["items"]:
        if item["kind"] == "Namespace":
            spaces.append(item["metadata"]["name"])
    return spaces

def get_pods(namespace):
    cmd_output = os.popen("{kubectl} get pods -n {namespace} -o json".format(kubectl = config["kubectl_command"], namespace=namespace)).read()
    json_output = json.loads(cmd_output)
    pods = []
    for item in json_output["items"]:
        if item["kind"] == "Pod":
            pod = {}
            pod["id"] = item["metadata"]["name"]
            pod["containers"] = []
            container = {}
            if "containerStatuses" in item["status"]:
                for state in item["status"]["containerStatuses"]:
                    container["ready"] = state["ready"]
                    container["name"] = state["name"]
                    container["image"] = state["image"]
                    if "running" in state["state"]:
                        container["start_time"] = state["state"]["running"]["startedAt"]
                    else:
                        container["start_time"] = ""
                    container["state"] = state["state"]
                    
                    
            else:
                container["ready"] = ""
                container["name"] = ""
                container["image"] = ""
                container["start_time"] = ""
                container["state"] = ""
            pod["containers"].append(container)
            pod["state"] = item["status"]["phase"]
            pods.append(pod)
    return pods

def get_services(namespace):
    cmd_output = os.popen("{kubectl} get services -n {namespace} -o json".format(kubectl = config["kubectl_command"], namespace=namespace)).read()
    json_output = json.loads(cmd_output)
    services = []
    for item in json_output["items"]:
        if item["kind"] == "Service":
            service = {}
            service["id"] = item["metadata"]["name"]
            if "common.k8s.elastic.co/type" in item["spec"]["selector"]:
                service["service_type"] = item["spec"]["selector"]["common.k8s.elastic.co/type"]
            else:
                service["service_type"] = ""
        
            service["type"] = item["spec"]["type"]
             
            service["internal_ip"] = item["spec"]["clusterIP"]
            service["ports"] = item["spec"]["ports"]
            host_access = "localhost"
            if config["local_cluster"] == "minikube":
                host_access = os.popen("minikube ip").read()
            if config["local_cluster"] == "microk8s":
                host_output = os.popen("microk8s.kubectl describe node $(microk8s.kubectl get nodes --no-headers | cut -f 1 -d " ") | grep InternalIP").read()
                host_access = host_output.split(":")[1].strip()
            if service["type"] == "NodePort":
                if "name" in item["spec"]["ports"][0]:
                    service["url"] = item["spec"]["ports"][0]["name"] + "://" + host_access + ":" + str(item["spec"]["ports"][0]["nodePort"])
            else:
                if "name" in item["spec"]["ports"][0]:
                    service["url"] = "" #item["spec"]["ports"][0]["name"] + "://" + service["internal_ip"] + ":" + str(item["spec"]["ports"][0]["port"])
            services.append(service)
    return services

def create_namespace(namespace):
    output = os.popen("{kubectl} create namespace {namespace}".format(kubectl = config["kubectl_command"], namespace = namespace)).read()
    return output
    
def get_elastic_password(namespace):
    deployment_name = namespace.split("-")[1]
    password = os.popen("{kubectl} get secret elasticsearch-{deployment_name}-es-elastic-user -o=jsonpath='{{.data.elastic}}' -n {namespace} | base64 --decode".format(kubectl = config["kubectl_command"], deployment_name=deployment_name, namespace=namespace)).read()
    return password

def deploy_full_stack(namespace, name, version):
    os.environ['ELASTIC'] = version
    os.environ['ECK_DEPLOYMENT_NAME'] = name
    os.environ['ECK_NAMESPACE'] = namespace
    yaml = os.popen("envsubst '$ELASTIC,$ECK_DEPLOYMENT_NAME,$ECK_NAMESPACE' < ./operator_templates/deploy_full_stack.yaml").read()
    output = os.popen("envsubst '$ELASTIC,$ECK_DEPLOYMENT_NAME,$ECK_NAMESPACE' < operator_templates/deploy_full_stack.yaml | {kubectl} apply -f - -n {namespace}".format(kubectl = config["kubectl_command"], namespace = namespace)).read()
    return output

def check_elastic_exists(namespace):
    cmd_output = os.popen("{kubectl} get elastic -o json".format(kubectl = config["kubectl_command"])).read()
    json_output = json.loads(cmd_output)
    return (len(json_output["items"]) > 0)

def remove_namespace(namespace):
    messages = []
    messages.append(os.popen("{kubectl} delete namespace {namespace}".format(kubectl = config["kubectl_command"], namespace=namespace)))
    return messages

def remove_stack(namespace):
    messages = []
    deployment_name = namespace.split("-")[1]
    messages.append(os.popen("{kubectl} delete elastic --all -n {namespace}".format(kubectl = config["kubectl_command"], namespace=namespace)))
    messages.append(os.popen("{kubectl} delete service apm-{deployment_name} -n {namespace}".format(kubectl = config["kubectl_command"], deployment_name=deployment_name, namespace=namespace)))
    return messages

def install_operator(version):
    messages = []
    messages.append(os.system("{kubectl} create -f https://download.elastic.co/downloads/eck/{operator}/crds.yaml".format(kubectl = config["kubectl_command"], operator = version)))
    messages.append(os.system("{kubectl} apply -f https://download.elastic.co/downloads/eck/{operator}/operator.yaml".format(kubectl = config["kubectl_command"], operator = version)))
    return messages

def get_config():
    global config
    if not bool(config):
        with open('config.json') as config_file:
            config = json.load(config_file)
    return config

def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)