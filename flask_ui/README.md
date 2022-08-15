# UI to deploy Elastic on a local cluter with operator already installed

* create python virtual environment

```bash
pip install -r requirements.txt

export FLASK_APP=app

flask --debug run
```

* access on : http://localhost:5000


## Tested on
* microk8s on Linux (PopOS/Ubuntu)
* minikube on Mac
* microk8s on Mac

## If using microk8s enable
```
addons:
  enabled:
    community            # (core) The community addons repository
    dashboard            # (core) The Kubernetes dashboard
    dns                  # (core) CoreDNS
    ha-cluster           # (core) Configure high availability on the current node
    hostpath-storage     # (core) Storage class; allocates storage from host directory
    metrics-server       # (core) K8s Metrics Server for API access to service metrics
    registry             # (core) Private image registry exposed on localhost:32000
    storage              # (core) Alias to hostpath-storage add-on, deprecated
```

## Todo
* Show version number in name space
* Show upgrade option if later version exists
* Add more config parameters
* Flexible template
