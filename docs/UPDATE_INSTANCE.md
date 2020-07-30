# Update an existing Instance

See docs/CREATE_INSTANCE.md to create the instance

Once instance is created you can refer to this doc to update / deploy it

## Deploy / update existing instance

```
export INSTANCE_NAME=demo
```

Update values and deploy

```
ckan-cloud-operator ckan instance update $INSTANCE_NAME \
    --override-spec-file /datacity-k8s/instances/$INSTANCE_NAME/values.yaml \
    --ckan-cloud-docker-latest-tag $(cat /datacity-k8s/instances/ckan-cloud-docker-latest-tag.txt) \
    --persist-overrides --wait-ready
```

## Add an external domain to the instance

Set a DNS CNAME from the external domain to `INSTANCE_NAME.datacity.org.il`

Edit the values and add an ingress rule for this domain

Update the instance
