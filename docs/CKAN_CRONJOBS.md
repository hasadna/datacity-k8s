# CKAN CronJobs

Some CKAN operations require periodical execution of commands on the CKAN instance

These tasks run via the Jenkins server and are described here

See the [JENKINS](/docs/JENKINS.md) doc for the template Jenkins task, it is assumed this is used to run the following tasks 

## Page views tracking

Should run daily

```
cd /datacity-k8s/instances &&\
RES=0 &&\
for INSTANCE_NAME in \$(ls --hide *.txt); do
    if cat \${INSTANCE_NAME}/values.yaml | grep 'enableCronJob_PageViewsTracking: true' >/dev/null; then
        if ! INSTANCE_ID=\$(kubectl -n ckan-cloud get ckancloudckaninstancename ckan-cloud-ckaninstancename-\$INSTANCE_NAME -o json | jq -r '.spec[\"latest-instance-id\"]') &&\
		     POD_NAME=\$(kubectl -n \$INSTANCE_ID get pods -l app=ckan -o json | jq -r \".items[0].metadata.name\") &&\
		     echo \$INSTANCE_ID \$POD_NAME &&\
		     kubectl -n \$INSTANCE_ID exec \$POD_NAME -- ckan-paster --plugin=ckan tracking -c /etc/ckan/production.ini update 2020-07-01 &&\
		     kubectl -n \$INSTANCE_ID exec \$POD_NAME -- ckan-paster --plugin=ckan search-index -c /etc/ckan/production.ini rebuild
        then
        	RES=1
        fi
    fi
done
```
