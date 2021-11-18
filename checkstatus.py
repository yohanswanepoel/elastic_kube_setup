import os
import sys
import platform


# Status elastic
os.system("kubectl get elasticsearches")

# Status APM
os.system("kubectl get apmservers")

# Status kibana
os.system("kubectl get kibanas")

# Status beats
os.system("kubectl get beats")

