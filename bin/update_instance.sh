#!/usr/bin/env bash

INSTANCE_NAME="${1}"
SERVICE_ACCOUNT_KEY_FILE="${2}"

[ "${INSTANCE_NAME}" == "" ] && echo missing INSTANCE_NAME && exit 1
[ "${SERVICE_ACCOUNT_KEY_FILE}" == "" ] && echo missing SERVICE_ACCOUNT_KEY_FILE && exit 1
! [ -e "instances/${INSTANCE_NAME}/values.yaml" ] && echo missing instance values && exit 1

bin/cco_exec.sh "${SERVICE_ACCOUNT_KEY_FILE}" "
ckan-cloud-operator ckan instance update ${INSTANCE_NAME} \
    --override-spec-file /datacity-k8s/instances/${INSTANCE_NAME}/values.yaml \
    --ckan-cloud-docker-latest-tag \$(cat /datacity-k8s/instances/ckan-cloud-docker-latest-tag.txt) \
    --persist-overrides --wait-ready
"