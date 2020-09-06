# Update an existing Instance

See docs/CREATE_INSTANCE.md to create a new instance

## Update values

Edit and update any instance values you want to change in instances/INSTANCE_NAME/values.yaml

Commit the modified values

## Deploy / update existing instance

Run the Jenkins job `update-instance`

## Add an external domain to the instance

Set a DNS CNAME from the external domain to `INSTANCE_NAME.datacity.org.il`

Edit the values and add an ingress rule for this domain

Deploy