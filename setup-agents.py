import os
import sys
import platform


# Installing the state-metrics-service
# this goes into the kube-system namespace
os.system("git clone https://github.com/kubernetes/kube-state-metrics.git kube-state-metrics"
os.system("kubectl create -f kube-state-metrics/examples/standard")
os.system("rm -rf kube-state-metrics")

# Setup metrics
os.system("kubectl apply -f metricbeat.yaml -n elk")

# Setup logs
os.system("kubectl apply -f filebeat.yaml -n elk")

# Setup logs
os.system("kubectl apply -f hearbeat.yaml -n elk")