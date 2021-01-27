# Create a Datacity Instance

## Create a Storage Bucket

Using Google Cloud Console, create a storage bucket for the instance:

* name: `datacity-INSTANCE_NAME`
* Location: region, europe-west1
* Storage Class: standard
* Permissions: fine-grained

Create a service account and HMAC key

* Cloud storage > Settings > Interoperability > Create a key for another service account
* Create new account, name: `datacity-storage-INSTANCE_NAME` (no roles)
* Keep the access key / secret

Give the service account permissions for the bucket

* Cloud Storage > Bucket > Permissions
* Add the service account with Storage Object Admin role

Set CORS on the bucket

```
gsutil cors set instances/cors-config.json gs://datacity-INSTANCE_NAME
``` 

## Set DNS

Create a DNS CNAME rule `INSTANCE_NAME.datacity.org.il` to `cluster-ingress.datacity.org.il` 

## Prepare the instance values

Instance values are stored in this repository under `instances/INSTANCE_NAME/values.yaml`

You can copy values from another instances and modify as needed

Commit the new instance values

## Create instance

Run the Jenkins job `create-instance`

## Update instance

See UPDATE_INSTANCE.md to deploy

## Create an admin user

Run the jenkins job `set-sysadmin` and create a user named `admin`, email can be `admin@localhost`

## Initialize instance

Login as the admin user to the instance and get the api key

Edit secret in hasadna cluster - namespace: `datacity`, secret name: `ckan-dgp-instances`

Add the following values (replace `NAME` with the instance name in upper-case with dashes converted to underscores):

* `CKAN_INSTANCE_NAME_URL` - the instance url `https://NAME.datacity.org.il`
* `CKAN_INSTANCE_NAME_API_KEY` - the admin user api key

Redeploy the ckan dgp server in hasadna cluster - namespace: `datacity`, deployment: `ckan-dgp`

Login to the ckan dgp server - https://ckan-dgp.datacity.org.il/

Create new processing tasks (replace NAME with the instance name):

* name: CITY NAME - initialize
  * Kind: initialize datacity ckan instances
  * ckan instance: NAME
  * main organization title: עיריית שם העיר
  * names of the municipality: write as many differently spelled names of the municipality
  * schedule: manual
  * visibility: public
  * View Status > Trigger Task
* name: CITY NAME - xlsx processing
  * Kind: continous processing tasks for datacity ckan instances
  * ckan instance: NAME
  * processing task to run: xlsx
  * schedule: hourly
  * visibility: public
  * View Status > Trigger Task
* name: CITY NAME - geojson processing
  * Kind: continous processing tasks for datacity ckan instances
  * ckan instance: NAME
  * processing task to run: geojson
  * schedule: hourly
  * visibility: public
  * View Status > Trigger Task

Create organization for the instance in מידע לעם - should be the same name and icon as the city organization in the instance.

organization description example: נתונים מתעדכנים אוטומטית מפורטל המידע של מעלה אדומים - https://maale-adummim.datacity.org.il/

Some municipalities already exist in odata as a group - in this case you should still create an organization but make sure the id (url slug) is different

For example - https://www.odata.org.il/organization/maale-adummim

Create a processing task in ckan-dgp:

* name: CITY NAME - sync to odata
  * kind: sync ckan instances
  * source: CITY NAME
  * target: odata
  * target organization ID: the id of the organization that you created
  * target ckan package name prefix: city_name_dgpsync_
  * target ckan package title prefix (example): "עיריית מעלה אדומים - " 
  * schedule: daily
  * visibility: public
  * View Status > Trigger Task
