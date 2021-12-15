import os
import sys
import platform


# create development namespace
os.system("kubectl create namespace development")

################################################################
#  Deploy MongoDB - shows nice metrics/logs    
################################################################
os.system("kubectl apply -f mongo_db/mongo_secret.yaml -n development")
os.system("kubectl apply -f mongo_db/mongo_service.yaml -n development")
os.system("kubectl apply -f mongo_db/mongo.yaml -n development")

##################################################################
#  Deploy Java Application - shows nice metrics/logs and APM data
##################################################################


# Setup security
os.system("""kubectl get secret apm-server-sample-apm-token -n elk -o json | jq --sort-keys \
            'del(
              .metadata.annotations."kubectl.kubernetes.io/last-applied-configuration",
              .metadata.annotations."control-plane.alpha.kubernetes.io/leader",
              .metadata.uid,
              .metadata.selfLink,
              .metadata.resourceVersion,
              .metadata.creationTimestamp,
              .metadata.generation,
              .metadata.namespace,
              .metadata.labels
          )' | kubectl apply --namespace=development -f -""")

# Deploy application
os.system("kubectl apply -f java_app/petclinic_with_apm.yaml -n development")
os.system("kubectl apply -f petclinic_service.yaml -n development")
os.system("minikube service petclinic -n development --url")
