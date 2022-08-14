import os
import sys
import platform
import config
import re
import config
import json

def get_namespaces():
    namespaces = os.popen("{kubectl} get namespace".format(kubectl = config.kubectl_command)).read()
    spaces = []
    lines = namespaces.split("\n")
    for line in lines[1:]:
        spaces.append(line.split(" ")[0])
    return spaces

def get_pods(namespace):
    cmd_output = os.popen("{kubectl} get pods -n {namespace} -o json".format(kubectl = config.kubectl_command, namespace=namespace)).read()
    json_output = json.loads(cmd_output)
    pods = []
    for item in json_output["items"]:
        if item["kind"] == "Pod":
            pod = {}
            pod["id"] = item["metadata"]["name"]
            pod["containers"] = []
            for state in item["status"]["containerStatuses"]:
                container = {}

                container["name"] = state["name"]
                container["image"] = state["image"]
                container["state"] = state["state"]
                
                pod["containers"].append(container)
            pod["state"] = item["status"]["phase"]
            pods.append(pod)
    return pods

def get_services(namespace):
    cmd_output = os.popen("{kubectl} get services -n {namespace} -o json".format(kubectl = config.kubectl_command, namespace=namespace)).read()
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
            
            if "agent.k8s.elastic.co/name" in item["spec"]["selector"]:
                service["elastic_component"] = item["spec"]["selector"]["agent.k8s.elastic.co/name"]
            else:
                service["elastic_component"] = ""
            service["type"] = item["spec"]["type"]
             
            service["internal_ip"] = item["spec"]["clusterIP"]
            service["ports"] = item["spec"]["ports"]
            if service["type"] == "NodePort":
                if "name" in item["spec"]["ports"][0]:
                    service["url"] = item["spec"]["ports"][0]["name"] + "://localhost:" + str(item["spec"]["ports"][0]["nodePort"])
            else:
                if "name" in item["spec"]["ports"][0]:
                    service["url"] = "" #item["spec"]["ports"][0]["name"] + "://" + service["internal_ip"] + ":" + str(item["spec"]["ports"][0]["port"])
            services.append(service)
    return services

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