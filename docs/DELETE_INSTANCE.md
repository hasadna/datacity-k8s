# Delete an instance

```
INSTANCE_NAME=demo
```

Get the instance ID

```
INSTANCE_ID="$(ckan-cloud-operator ckan instance get ${INSTANCE_NAME} | grep '^id: ' | cut -d" " -f2)"
```

Delete the instance

```
ckan-cloud-operator ckan instance delete $INSTANCE_ID --no-dry-run
```

Delete route

```
ROUTE_ID="$(kubectl -n ckan-cloud get ckancloudroute -l ckan-cloud/route-ckan-instance-id=$INSTANCE_ID '-o=jsonpath={.items[0].spec.name}')"
kubectl -n ckan-cloud delete ckancloudroute $ROUTE_ID
```

Update the router

```
ckan-cloud-operator routers update instances-default
```

Delete additional resources

```
kubectl -n ckan-cloud delete secret ckan-instance-$INSTANCE_NAME
kubectl -n ckan-cloud delete ckancloudckaninstancename ckan-cloud-ckaninstancename-${INSTANCE_NAME}
```

Delete the Google Storage bucket
