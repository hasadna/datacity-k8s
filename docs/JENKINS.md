# Jenkins Automation

Jenkins is used to provide secure automation and self-management

## Jenkins Jobs

Following is a common Jenkins job for performing any cluster operation:

```
#!/usr/bin/env bash

[ "${INSTANCE_NAME}" == "" ] && echo missing INSTANCE_NAME && exit 1
! [ -e "instances/${INSTANCE_NAME}/values.yaml" ] && echo missing instance values && exit 1

export CCO_DIR=`mktemp -d` &&\
cp $SERVICE_ACCOUNT_KEY_FILE $CCO_DIR/service_account_key.json &&\
docker pull datacity/ckan-cloud-operator &&\
docker run -v "${CCO_DIR}:/root/" -v "$(pwd):/datacity-k8s" datacity/ckan-cloud-operator -c "
gcloud auth activate-service-account --key-file=/root/service_account_key.json &&\
gcloud config set project datacity-k8s &&\
gcloud container clusters get-credentials datacity --zone europe-west1-d &&\
helm init -c &&\
ckan-cloud-operator ckan instance update ${INSTANCE_NAME} \
    --override-spec-file /datacity-k8s/instances/${INSTANCE_NAME}/values.yaml \
    --persist-overrides --wait-ready
"
RES=$?
rm -rf $CCO_DIR
exit $RES
``` 

## Running a job with parameters remotely

Create an automation user, and get it's token (From the user's configure page)

Set env vars:

```
JENKINS_USER=
JENKINS_TOKEN=
JENKINS_JOB_URL="https://${JENKINS_DOMAIN}/.../buildWithParameters?INSTANCE_NAME="
```

Run the job

```
curl --user "${JENKINS_USER}:${JENKINS_TOKEN}" \
     -X POST "${JENKINS_JOB_URL}"
```
