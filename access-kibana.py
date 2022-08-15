import os
import sys
import platform
import config


os.system("{kubectl} config set-context --current --namespace=elk".format(kubectl =config.kubectl_command))
# Get elastic password

pw = os.popen("{kubectl} get secret elasticsearch-sample-es-elastic-user -o=jsonpath='{{.data.elastic}}' -n elk | base64 --decode".format(kubectl = config.kubectl_command)).read()
print("Elastic Password: ")
print(pw)
# Expose the port
#print("Access Kibana at https://localhost:5601")
#os.system("{kubectl} port-forward service/kibana-sample-kb-http 5601".format(kubectl =config.kubectl_command))