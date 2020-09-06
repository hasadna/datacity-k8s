#!/usr/bin/env bash

INSTANCE_NAME="${1}"
S3_FILESTORE_AWS_BUCKET_NAME="${2}"
S3_FILESTORE_AWS_ACCESS_KEY_ID="${3}"
S3_FILESTORE_AWS_SECRET_ACCESS_KEY="${4}"
SERVICE_ACCOUNT_KEY_FILE="${5}"

[ "${INSTANCE_NAME}" == "" ] && echo missing INSTANCE_NAME && exit 1
[ "${SERVICE_ACCOUNT_KEY_FILE}" == "" ] && echo missing SERVICE_ACCOUNT_KEY_FILE && exit 1
! [ -e "instances/${INSTANCE_NAME}/values.yaml" ] && echo missing instance values && exit 1
( [ "${S3_FILESTORE_AWS_ACCESS_KEY_ID}" == "" ] || [ "${S3_FILESTORE_AWS_SECRET_ACCESS_KEY}" == "" ] || [ "${S3_FILESTORE_AWS_BUCKET_NAME}" == "" ] ) && echo missing S3 values && exit 1

bin/cco_exec.sh "${SERVICE_ACCOUNT_KEY_FILE}" "
( kubectl -n ckan-cloud create secret generic ckan-instance-${INSTANCE_NAME} \
    --from-literal S3_FILESTORE_AWS_HOST_NAME=https://storage.googleapis.com \
    --from-literal S3_FILESTORE_AWS_ACCESS_KEY_ID=${S3_FILESTORE_AWS_ACCESS_KEY_ID} \
    --from-literal S3_FILESTORE_AWS_SECRET_ACCESS_KEY=${S3_FILESTORE_AWS_SECRET_ACCESS_KEY} \
    --from-literal S3_FILESTORE_AWS_BUCKET_NAME=${S3_FILESTORE_AWS_BUCKET_NAME} \
    --from-literal S3_FILESTORE_AWS_REGION_NAME=europe-west1 || true ) &&\
ckan-cloud-operator ckan instance create helm \
    --instance-name ${INSTANCE_NAME} \
    /datacity-k8s/instances/${INSTANCE_NAME}/values.yaml
"