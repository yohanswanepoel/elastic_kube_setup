import os
import sys
import platform
import config


print ("Operator Version: {}".format(config.version['OPERATOR']))
print ("Elastic Version: {}".format(config.version['ELASTIC']))

os.environ['ELASTIC'] = config.version['ELASTIC']

# Do we need to clean up first
os.system("kubectl create namespace elk")
os.system("kubectl config set-context --current --namespace=elk")

# Install the operator
os.system("kubectl create -f https://download.elastic.co/downloads/eck/{}/crds.yaml".format(config.version['OPERATOR']))
os.system("kubectl apply -f https://download.elastic.co/downloads/eck/{}/operator.yaml".format(config.version['OPERATOR']))

# Install Elastic Stack - Search, Kibana, APM
os.system("envsubst '$ELASTIC' < deploy_full_stack.yaml | kubectl apply -f - -n elk")

os.system("minikube service apm-external -n elk --url")