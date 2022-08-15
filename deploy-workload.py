import os
import sys
import platform
import config

print ("Elastic JAVA APM Version: {}".format(config.version['APM_JAVA']))

os.environ['APM_JAVA'] = config.version['APM_JAVA']


# create development namespace
os.system("{kubectl} create namespace development".format(kubectl=config.kubectl_command))

################################################################
#  Deploy MongoDB - shows nice metrics/logs    
################################################################
os.system("{kubectl} apply -f mongo_db/mongo_secret.yaml -n development".format(kubectl=config.kubectl_command))
os.system("{kubectl} apply -f mongo_db/mongo_service.yaml -n development".format(kubectl=config.kubectl_command))
os.system("{kubectl} apply -f mongo_db/mongo.yaml -n development".format(kubectl=config.kubectl_command))

##################################################################
#  Deploy Java Application - shows nice metrics/logs and APM data
##################################################################


# Setup security
# os.system("""{kubectl} get secret apm-server-sample-apm-token -n {elk_namespace} -o json | jq --sort-keys \
#             'del(
#               .metadata.annotations."kubectl.kubernetes.io/last-applied-configuration",
#               .metadata.annotations."control-plane.alpha.kubernetes.io/leader",
#               .metadata.uid,
#               .metadata.selfLink,
#               .metadata.resourceVersion,
#               .metadata.creationTimestamp,
#               .metadata.generation,
#               .metadata.namespace,
#               .metadata.labels
#           )' | {kubectl2} apply --namespace=development -f -""".format(kubectl=config.kubectl_command, elk_namespace=config.namespace, kubectl2=config.kubectl_command))

# Deploy application
os.system("envsubst '$APM_JAVA' < java_app/petclinic_with_apm.yaml | {kubectl} apply -f - -n development".format(kubectl=config.kubectl_command))
os.system("{kubectl} apply -f java_app/petclinic_service.yaml -n development".format(kubectl=config.kubectl_command))
#os.system("minikube service petclinic -n development --url")
