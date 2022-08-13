import os
import sys
import platform
import config


os.system("{kubectl} config set-context --current --namespace=elk".format(kubectl =config.kubectl_command))
# Get elastic password
print("Elastic Password: ")
os.system("echo `microk8s.kubectl get secret elasticsearch-sample-es-elastic-user -o=jsonpath='{.data.elastic}' -n elk | base64 --decode`")

# Expose the port
print("Access Kibana at https://localhost:5601")
os.system("{kubectl} port-forward service/kibana-sample-kb-http 5601".format(kubectl =config.kubectl_command))