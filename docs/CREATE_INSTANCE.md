# Create a Datacity Instance

## Create a Storage Bucket

Using Google Cloud Console, create a storage bucket for the instance:

* name: `datacity-INSTANCE_NAME`
* Location: region, europe-west1
* Storage Class: standard
* Permissions: fine-grained

Create a service account and HMAC key

* Cloud storage > Settings > Interoperability > Create a key for another service account
* Create new account, name: `datacity-storage-INSTANCE_NAME` (no roles)
* Keep the access key / secret

Give the service account permissions for the bucket

* Cloud Storage > Bucket > Permissions
* Add the service account with Storage Object Admin role

Set CORS on the bucket

```
gsutil cors set instances/cors-config.json gs://datacity-INSTANCE_NAME
``` 

## Set DNS

Create a DNS CNAME rule `INSTANCE_NAME.datacity.org.il` to `cluster-ingress.datacity.org.il` 

## Prepare the instance values

Instance values are stored in this repository under `instances/INSTANCE_NAME/values.yaml`

You can copy values from another instances and modify as needed

Commit the new instance values

## Create instance

Run the Jenkins job `create-instance`

## Update instance

See UPDATE_INSTANCE.md to continue deployment