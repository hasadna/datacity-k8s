# Update an existing Instance

See docs/CREATE_INSTANCE.md to create a new instance

## Update values

Edit and update any instance values you want to change in instances/INSTANCE_NAME/values.yaml

Commit the modified values

## Monitor cluster

Open Google Cloud Console Monitoring dashboard `datacity-k8s > datacity cluster`

Open Rancher or Lens connected to the cluster

While deploying check the cpu/ram usage and deployment progress to ensure the instance does not overload the cluster 

## Deploy / update existing instance

Run the Argo Workflows template `cco-update-instance` under `datacity` namespace with recreate helm = true.

If the job failed, try to re-run a couple of time before panicking

## Add an external domain to the instance

Set a DNS CNAME from the external domain to `INSTANCE_NAME.datacity.org.il`

Edit the values and add an ingress rule for this domain

Deploy

If you had existing resources on the instance, run jenkins job reindex-solr
