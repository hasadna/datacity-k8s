# Connect to ckan-cloud-operator from local PC

## Prepare directories

You should have the following directory structure:

* `./datacity-k8s` - clone of `hasadna/datacity-k8s` repository, `master` branch
* `./ckan-cloud-operator` - clone of `hasadna/ckan-cloud-operator` repository, `master` branch

You should also have a secret working directory to store persistent operator data

Keep this path safe and outside of the repositories

Copy the secret service account for the cluster to service_account_key.json inside this directory

## Run the operator shell

Set the secret cco path in an env var

```
export CCO_DIR=/path/to/secret/cco
```

Build and run the operator (run it from within one of the repos)

```
docker pull datacity/ckan-cloud-operator &&\
docker run -it -v "${CCO_DIR}:/root/" \
               -v "$(pwd)/../datacity-k8s:/datacity-k8s" \
               datacity/ckan-cloud-operator
```

Following should run only once, every time you have a new cco secret path

```
gcloud auth activate-service-account --key-file=/root/service_account_key.json
gcloud config set project datacity-k8s
gcloud container clusters get-credentials datacity --zone europe-west1-d
helm init -c
```

Run the following each time you start a new ckan-cloud-operator shell:

```
pip install -e .
eval "$(ckan-cloud-operator bash-completion)"
```

## Running the operator for development

```
docker build -t datacity/ckan-cloud-operator \
             -f ../ckan-cloud-operator/Dockerfile.gcloud \
             ../ckan-cloud-operator &&\
docker run -it -v "$(pwd)/../ckan-cloud-operator:/cco" \
               -v "${CCO_DIR}:/root/" \
               -v "$(pwd)/../datacity-k8s:/datacity-k8s" \
               datacity/ckan-cloud-operator
```

## Testing helm chart changes

Clone the ckan-cloud-helm repo

Set the chart in the relevant site's values:

```
ckanHelmChartRepo: file
ckanHelmChartVersion: /ckan-cloud-helm/ckan
```

Mount ckan-cloud-helm into the operator container:

```
-v "$(pwd)/../ckan-cloud-helm:/ckan-cloud-helm"
```
