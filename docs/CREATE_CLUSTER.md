# Create the datacity cluster

## Prerequisites

All infra created in Google project: `datacity-k8s`

Use the Google Kubernetes Engine web-ui to create a Kubernetes cluster

* Cluster name: `datacity`
* Location type: Zonal, europe-west1-d
* Master Version: 1.16.10-gke.8
* Number of nodes: 1
* Auto Upgrade: off
* Machine type: Container-optimized OS, e2-standard-2

Use the Google Cloud SQL web-ui to create a database

* PostgreSQL
* Instance ID: `datacity-cc1`
* Zone: `europe-west1-d`
* Database Version: PostgreSQL 9.6
* Connect using private IP only
* Machine type: 1vCPU, 3.75GM RAM
* Storage type: SSD 10GB, enable automatic increase

Deploy an NFS server - 

* Create a compute instance (`datacity-nfs`)
* SSH to setup NFS:

```
apt-get update && apt-get install -y nfs-kernel-server &&\
chown -R nobody:nogroup /exports &&\
echo '/exports 10.0.0.0/8(rw,sync,no_subtree_check,no_root_squash,fsid=0)' >> /etc/exports &&\
exportfs -a &&\
systemctl restart nfs-kernel-server
```

* Create a test directory and file: `mkdir /exports/test && echo hello world > /exports/test/test.txt`
* Try to mount using the external IP from external host - to ensure it doesn't work

Create a Google Cloud service account

* IAM > Service accounts > Create service account
* Name: `datacity-ckan-cloud-operator`
* Service account ID: `datacity-ckan-cloud-operator`
* Role: Project Viewer
* Role: Compute Admin
* Create JSON Key
* Save it securely

Authenticate with Gcloud and connect to the cluster with your admin account (not the service account)

```
gcloud auth login
gcloud config set project datacity-k8s
gcloud container clusters get-credentials datacity --zone europe-west1-d
```

Give the service account full cluster admin permissions:

```
kubectl create clusterrolebinding cc-cluster-admin-binding \
  --clusterrole cluster-admin \
  --user SERVICE_ACCOUNT_EMAIL
```

Add the cluster to Rancher - follow instructions in Rancher's UI

## Initialize ckan-cloud-operator

```
ckan-cloud-operator cluster initialize --interactive --cluster-provider=gcloud
```

* Service account JSON path: `/root/service_account.json` (the filename you saved the service account json key to)
* Service account email: `datacity-ckan-cloud-operator@datacity-k8s.iam.gserviceaccount.com`
* Cluster compute zone: `europe-west1-d`
* Cluster name: `datacity`
* Project ID: `datacity-k8s`
* GcloudSQL host: the internal IP of the GcloudSQL instance
* port: (default()
* is-private-ip: (default)
* admin-user / password: use the values for the GcloudSQL instance root / postgres user
* GcloudSQL instance name: `datacity-cc1`
* env-id: `p`
* default-root-domain: `odata.org.il`
* dns-provider: `cloudflare`
* cloudflare email: `api-token`
* cloudflare api key: api token limited to DNS editing of the default root domain zone
* sc cpu/mem: `.5` / `1Gi`
* zk cpu/mem: keep default
* zn cpu/mem: keep default
* sc cpu/mem limit: `1.5` / `1.5Gi`
* zk cpu/mem limit: keep default
* zn cpu/mem limit: keep default
* sc suffixes: `sc-7`
* zk suffixes: `zk-4`
* replication-factor: `1`

## Install nginx ingress

Install nginx ingress

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.30.0/deploy/static/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.30.0/deploy/static/provider/cloud-generic.yaml
```

Verify ingress-nginx is Running

```
kubectl get pods --all-namespaces -l app.kubernetes.io/name=ingress-nginx
```

Get the external IP

```
kubectl get -n ingress-nginx service
```

Make sure to add the following annotation to all ingresses:

```
kubernetes.io/ingress.class: "nginx"
```

Install cert-manager for SSL

```
kubectl create ns cert-manager
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.13.0/cert-manager.yaml
kubectl get pods --namespace cert-manager
```

Create lets-encrypt cluster issuer

Create a Let's Encrypt cluster issuer (replace the email with your email):

```
echo "apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt
  namespace: cert-manager
spec:
  acme:
    email: user@example.com
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      # Secret resource used to store the account's private key.
      name: cluster-issuer-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
" | kubectl apply -f -
```

To use, add an ingress, for example (replace NAME, NAMESPACE, HOSTNAME, SERVICENAME):

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: letsencrypt
  name: NAME
  namespace: NAMESPACE
spec:
  rules:
  - host: HOSTNAME
    http:
      paths:
      - backend:
          serviceName: SERVICENAME
          servicePort: 80
  tls:
  - hosts:
    - HOSTNAME
    secretName: NAME-cert
```