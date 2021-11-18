import os
import sys
import platform

# Setup metrics
os.system("kubectl apply -f metricbeat.yaml -n elk")

# Setup logs
os.system("kubectl apply -f filebeat.yaml -n elk")

# Setup logs
os.system("kubectl apply -f hearbeat.yaml -n elk")