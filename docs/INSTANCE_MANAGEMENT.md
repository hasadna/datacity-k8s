# Instance Management

Followin are commands which should be run on the relevant instance's CKAN pod, most operations should run via the relevant Jenkins job

## Set user password

```
ckan-paster --plugin=ckan user --config /etc/ckan/production.ini setpass USERNAME
```

## Xloader

Submit all resources to reprocess with xloader 

Jenkins job `xloader`

```
ckan-paster --plugin=ckanext-xloader xloader -c /etc/ckan/production.ini submit all
```

## SOLR Reindex

Jenkins job `solr-reindex`

```
ckan-paster --plugin=ckan search-index -c /etc/ckan/production.ini rebuild
```

## Set sysadmin

Jenkins job `set-sysadmin`

```
if [ \"${NEW_SYSADMIN_EMAIL}\" == \"\" ]; then
  kubectl -n \$INSTANCE_ID exec \$POD_NAME -- ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add $SYSADMIN_NAME
else
  echo y | kubectl -n \$INSTANCE_ID exec -i \$POD_NAME -- ckan-paster --plugin=ckan sysadmin -c /etc/ckan/production.ini add $SYSADMIN_NAME email=$NEW_SYSADMIN_EMAIL password=$NEW_SYSADMIN_PASSWORD
fi
```
