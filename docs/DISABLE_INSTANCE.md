# Temporarily Disable an instance

Rename the instance folder under `instances/` to `instances/INSTANCE_NAME.disabled` and commit the change.

Remove the instance namespace in Kubernetes

Re-apply hasadna-iac terraform to apply the changes (See repo hasadna/hasadna-iac for more details)
