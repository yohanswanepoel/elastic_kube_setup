import os
import sys
import platform
import config

print ("Elastic Version: {}".format(config.version['ELASTIC']))

os.environ['ELASTIC'] = config.version['ELASTIC']

# Installing the state-metrics-service
# this goes into the kube-system namespace
os.system("git clone https://github.com/kubernetes/kube-state-metrics.git kube-state-metrics")
os.system("{kubectl} create -f kube-state-metrics/examples/standard".format(kubectl=config.kubectl_command))
os.system("rm -rf kube-state-metrics")



# Setup metrics
os.system("envsubst '$ELASTIC' < metricbeat.yaml | {kubectl} apply -f - -n {namespace}".format(kubectl=config.kubectl_command, namespace=config.namespace))

# Setup logs
os.system("envsubst '$ELASTIC' < filebeat.yaml | {kubectl} apply -f - -n {namespace}".format(kubectl=config.kubectl_command. namespace=config.namespace))

# Setup uptime
# os.system("kubectl apply -f hearbeat.yaml -n elk")