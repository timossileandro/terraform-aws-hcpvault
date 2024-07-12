# Setting up vault variables
export VAULT_ADDR="http://127.0.0.1:8200"
export VAULT_NAMESPACE="admin"
export VAULT_TOKEN="hvs.ATOKEN123456ABC"


# Configuring AWS Auth method
vault auth enable aws
vault write auth/aws/config/client secret_key="AWS_SECRET_KEY" access_key="AWS_ACCESS_KEY"
vault write auth/aws/role/a-role-name \
     auth_type=iam \
     bound_iam_principal_arn=arn:aws:iam::<YourAWSAccountID>:role/a-role-name \
     policies=an-acl-policy-name # check 'acl_policy.hcl'


# Verify configurations
vault read auth/aws/config/client 
vault read auth/aws/role/a-role-name