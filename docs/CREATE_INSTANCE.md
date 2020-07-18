# Create a Datacity Instance

## Create a Storage Bucket

Using Google Cloud Console, create a storage bucket for the instance:

* name: `datacity-INSTANCE_NAME`
* Location: region, europe-west1
* Storage Class: standard
* Permissions: fine-grained

Create a service account to access the bucket:

* name: `datacity-INSTANCE_NAME-storage`
* No roles

Create an HMAC key for the service account:

* Cloud storage > Settings > Interoperability
* Create HMAC key for service account

Give the service account permissions for the bucket

* Cloud Storage > Bucket > Permissions
* Add the service account with Storage Object Admin role

Create a secret with the bucket values:

```
kubectl -n ckan-cloud create secret generic ckan-instance-INSTANCE_NAME \
    --from-literal S3_FILESTORE_AWS_HOST_NAME= \
    --from-literal S3_FILESTORE_AWS_ACCESS_KEY_ID= \
    --from-literal S3_FILESTORE_AWS_SECRET_ACCESS_KEY= \
    --from-literal S3_FILESTORE_AWS_BUCKET_NAME= \
    --from-literal S3_FILESTORE_AWS_REGION_NAME=
```

## Prepare the instance values

Instance values are stored in this repository under `instances/INSTANCE_NAME/values.yaml`

You can copy values from another instances and modify as needed

## Create instance

Set instance name in env var

```
INSTANCE_NAME=demo
```

Create the instance custom resource

```
ckan-cloud-operator ckan instance create helm \
    --instance-name "${INSTANCE_NAME}" \
    /root/instances/$INSTANCE_NAME/values.yaml
```

See UPDATE_INSTANCE.md to continue deployment