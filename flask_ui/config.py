version=dict(
    OPERATOR="2.3.0",
    ELASTIC="8.3.3",
    APM_JAVA="1.29.0",
)

operator_versions = ["2.3.0","2.2.0"]

#kubectl_command = "kubectl"
kubectl_command = "microk8s.kubectl"

#local_cluster = "minikube"
local_cluster = "microk8s"

#namespace
namespace = "elk"
dev_namespace = "development"

versions = ["7.17.1","8.3.3","8.4.0"]
