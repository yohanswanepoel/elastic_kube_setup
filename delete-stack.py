import os
import sys
import platform
import config


print ("Operator Version: {}".format(config.version['OPERATOR']))
print ("Elastic Version: {}".format(config.version['ELASTIC']))

os.environ['ELASTIC'] = config.version['ELASTIC']

# Do we need to clean up first
# os.system("{kubectl} create namespace elk".format(kubectl = config.kubectl_command))
os.system("{kubectl} config set-context --current --namespace=elk".format(kubectl = config.kubectl_command))


os.system("{kubectl} delete elasticsearch/elasticsearch-sample".format(kubectl = config.kubectl_command))
os.system("{kubectl} delete kibana/kibana-sample".format(kubectl = config.kubectl_command))
os.system("{kubectl} delete agent/elastic-agent".format(kubectl = config.kubectl_command))
os.system("{kubectl} delete agent/fleet-server-sample".format(kubectl = config.kubectl_command))


os.system("{kubectl} delete namespace elk".format(kubectl = config.kubectl_command))



