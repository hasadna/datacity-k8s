# Connect to an instance CKAN Database

execute shell on the ckan pod and run:

```
. /etc/ckan-conf/secrets/secrets.sh
psql $SQLALCHEMY_URL
```
