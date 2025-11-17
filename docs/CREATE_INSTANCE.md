# Create a Datacity Instance

## Prepare the instance values

Instance values are stored in this repository under `instances/INSTANCE_NAME/values.yaml`

You can copy values from another instances and modify as needed

Commit the new instance values

## Deploy hasadna-iac Terraform

Apply hasadna-iac terraform - it should pickup the new instance and create the necessary resources

See hasadna/nasadna-iac repo for details

## Create instance

Go to https://argo.hasadna.org.il/ login via SSO

Workflow Templates -> namespace: `datacity` -> `cco-create-instance` -> Submit with following values:

* `INSTANCE_NAME` - the instance name
* `S3_FILESTORE_AWS_BUCKET_NAME` - `datacity-INSTANCE_NAME`
* `S3_FILESTORE_AWS_ACCESS_KEY_ID` / `S3_FILESTORE_AWS_SECRET_ACCESS_KEY` - from vault path `Projects/datacity/sites/INSTANCE_NAME/storage-iac`

## Update instance

See UPDATE_INSTANCE.md to deploy

## Create an admin user

Run the jenkins job `set-sysadmin` and create a user named `admin`, email can be `admin@localhost`

Store the password in Hasadna's vault under `Projects/datacity/sites/INSTANCE_NAME/ckan-admin`: `username` / `password`

## Initialize instance

Login as the admin user to the instance and get the api key

Edit secret in hasadna cluster - namespace: `datacity`, secret name: `ckan-dgp-instances`

Add the following values (replace `NAME` with the instance name in upper-case with dashes converted to underscores):

* `CKAN_INSTANCE_NAME_URL` - the instance url `https://NAME.datacity.org.il`
* `CKAN_INSTANCE_NAME_API_KEY` - the admin user api key

Redeploy the ckan dgp server in hasadna cluster - namespace: `datacity`, deployment: `ckan-dgp`

Login to the ckan dgp server - https://ckan-dgp.datacity.org.il/

Create new processing task (replace NAME with the instance name):

* name: CITY NAME - initialize
  * Kind: initialize datacity ckan instances
  * ckan instance: NAME
  * main organization title: עיריית שם העיר
  * names of the municipality: write as many differently spelled names of the municipality
  * schedule: manual
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

## Update Workflows

Edit in this repo `workflows/values.yaml` and add the instance name under `continuousProcessingTasksInstanceWorkflows`, commit & push
