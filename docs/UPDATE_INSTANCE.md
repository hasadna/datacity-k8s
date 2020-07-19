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
    --persist-overrides --wait-ready
```

## Add an external domain to the instance

```
export INSTANCE_NAME=demo
```

Get the instance ID

```
INSTANCE_ID="$(ckan-cloud-operator ckan instance get ${INSTANCE_NAME} | grep '^id: ' | cut -d" " -f2)"
```

Get the frontend hostname

```
ckan-cloud-operator routers get-routes --ckan-instance-id $INSTANCE_ID
```

Set a CNAME from the external domain to the frontend hostname

Edit the route

```
ROUTE_ID="$(kubectl -n ckan-cloud get ckancloudroute -l ckan-cloud/route-ckan-instance-id=$INSTANCE_ID '-o=jsonpath={.items[0].spec.name}')"
kubectl -n ckan-cloud edit ckancloudroute $ROUTE_ID
```

Add the following to the spec:

```
extra-external-domains:
- the.external.domain
```

Edit the instance values (`instances/INSTANCE_NAME/values.yaml`), set:

```
forceKeepSiteUrl: true
siteUrl: https://the.external.domain 
``` 

Update the instance
