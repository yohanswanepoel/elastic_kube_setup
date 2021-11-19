# TLDR: Setting up a full Elastic Stack 

https://operatorhub.io/operator/elastic-cloud-eck#:~:text=Elastic%20Cloud%20on%20Kubernetes%20(ECK,Elastic%20Maps%20Server%20on%20Kubernetes.


* Follow this read me or run
* Resources are setup in the *elk* namespace, to make it easy to clean things up.
```
# install the stack and expose kibana port
python3 install-stack.py

# setup agents
python3 setup-agents.py

# once running get access to Kibana
python3 access-kibana.py

```

## Install the CRD

You might want to look for later versions
```bash
kubectl create -f https://download.elastic.co/downloads/eck/1.8.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/1.8.0/operator.yaml
```

See the operator logs
```bash
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```

Understand the CRD
```bash
kubectl describe crd elasticsearch
```



## Setup
Deploy the full stack using the operator
```bash
kubectl create namespace elk

kubectl config set-context --current --namespace=elk

kubectl apply -f deploy_full_stack.yaml
```

Check the status
```bash
kubectl get elasticsearch,kibana,apmserver
```

Get access to the Kibana Dashboard
```bash
kubectl port-forward service/kibana-sample-kb-http 5601
```

Access the portal: https://localhost:5601/

Get the secret for user 'elastic'
```bash
echo `kubectl get secret elasticsearch-sample-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode`
```

## Install some beats

### Install Kube State Metrics to expose metrics in an easy to consume way
https://github.com/kubernetes/kube-state-metrics
```bash
git clone https://github.com/kubernetes/kube-state-metrics.git kube-state-metrics 
kubectl create -f kube-state-metrics/examples/standard
rm -rf kube-state-metrics
```

### Now let's setup the beats
```bash
    # Heartbeat specifically for Elastic
    kubectl apply -f hearbeat.yaml -n elk
    kubectl apply -f filebeat.yaml -n elk
    kubectl apply -f metricbeat.yaml -n elk
```

See some details on how your operator is doing
```bash
kubectl describe beats/filebeat 
```