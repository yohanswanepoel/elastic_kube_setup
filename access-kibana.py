import os
import sys
import platform


os.system("kubectl config set-context --current --namespace=elk")
# Get elastic password
print("Elastic Password: ")
os.system("echo `kubectl get secret elasticsearch-sample-es-elastic-user -o=jsonpath='{.data.elastic}' -n elk | base64 --decode`")

# Expose the port
print("Access Kibana at https://localhost:5601")
os.system("kubectl port-forward service/kibana-sample-kb-http 5601")