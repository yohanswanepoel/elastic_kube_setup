import os
import sys
import platform

OPERATOR_VERSION="1.8.0"
ELASTIC_VERSION="7.15.2"

# Do we need to clean up first

os.system("kubectl create namespace elk")
os.system("kubectl config set-context --current --namespace=elk")

# Install the operator
os.system("kubectl create -f https://download.elastic.co/downloads/eck/{}/crds.yaml".format(OPERATOR_VERSION))
os.system("kubectl apply -f https://download.elastic.co/downloads/eck/{}/operator.yaml".format(OPERATOR_VERSION))

# Install Elastic Stack - Search, Kibana, APM
os.system("kubectl apply -f deploy_full_stack.yaml -n elk")



