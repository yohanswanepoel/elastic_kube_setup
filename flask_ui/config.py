version=dict(
    OPERATOR="2.3.0",
    ELASTIC="8.3.3",
    APM_JAVA="1.29.0",
)

#kubectl_command = "kubectl"
kubectl_command = "microk8s.kubectl"

#namespace
namespace = "elk"
dev_namespace = "development"

versions = ["7.17.1","8.3.3","8.4.0"]