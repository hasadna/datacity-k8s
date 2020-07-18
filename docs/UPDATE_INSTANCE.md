# Update an existing Instance

See docs/CREATE_INSTANCE.md to create the instance

Once instance is created you can refer to this doc to update / deploy it

## Deploy / update existing instance

Set instance name in env var

```
export INSTANCE_NAME=demo
```

Update values and deploy

```
ckan-cloud-operator ckan instance update $INSTANCE_NAME \
    --override-spec-file /datacity-k8s/instances/$INSTANCE_NAME/values.yaml \
    --persist-overrides --wait-ready
```
