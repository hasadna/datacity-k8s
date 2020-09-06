#!/usr/bin/env bash

SERVICE_ACCOUNT_KEY_FILE="${1}"
EXEC_SCRIPT="${2}"

[ "${SERVICE_ACCOUNT_KEY_FILE}" == "" ] && echo missing SERVICE_ACCOUNT_KEY_FILE && exit 1
[ "${EXEC_SCRIPT}" == "" ] && echo missing EXEC_SCRIPT && exit 1

export CCO_DIR=`mktemp -d` &&\
cp $SERVICE_ACCOUNT_KEY_FILE $CCO_DIR/service_account_key.json &&\
docker pull datacity/ckan-cloud-operator &&\
docker run -v "${CCO_DIR}:/root/" -v "$(pwd):/datacity-k8s" datacity/ckan-cloud-operator -c "
gcloud auth activate-service-account --key-file=/root/service_account_key.json &&\
gcloud config set project datacity-k8s &&\
gcloud container clusters get-credentials datacity --zone europe-west1-d &&\
helm init -c &&\
${EXEC_SCRIPT}
"
RES=$?
rm -rf $CCO_DIR
exit $RES
