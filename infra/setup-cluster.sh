#!/bin/bash
set -e

CLUSTER_NAME="smartsupport-cluster"
REGISTRY_NAME="kind-registry"
REGISTRY_PORT="5001"

# 1. Create local registry if not exists
if [ "$(docker inspect -f '{{.State.Running}}' "${REGISTRY_NAME}" 2>/dev/null || true)" != 'true' ]; then
  docker run \
    -d --restart=always -p "127.0.0.1:${REGISTRY_PORT}:5000" --network bridge --name "${REGISTRY_NAME}" \
    registry:2
fi

# 2. Create KIND cluster with registry config
kind create cluster --name "${CLUSTER_NAME}" --config infra/kind-config.yaml

# 3. Connect registry to cluster network
docker network connect "kind" "${REGISTRY_NAME}" || true

# 4. Document the registry for kubectl
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:${REGISTRY_PORT}"
    help: "https://kind.sigs.k8s.io/docs/user/local-registry/"
EOF

echo "✅ KIND Cluster '${CLUSTER_NAME}' is ready with Local Registry at localhost:${REGISTRY_PORT}"
