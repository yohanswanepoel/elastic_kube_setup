import os
import sys
import platform


os.system("kubectl config set-context --current --namespace=elk")
print("Access APM")
os.system("minikube service apm-external -n elk --url")

print("Access APM at localhost:8200")
os.system("kubectl port-forward service/apm 8200")