variable "region" {
  type        = string
  description = "AWS Region name"
  default     = "ap-southeast-2"
}

variable "env" {
  type        = string
  description = "Environment of the resources"
  default     = "dev"
}

variable "application" {
  type        = string
  description = "Name of application"
  default     = "vault"
}

variable "layer_name" {
  type        = string
  description = "Name of the Layer to be used by Python functions."
  default     = "AWSSDKPandas-Python312"
}

variable "sns_email" {
  type        = string
  description = "Email address to be notified when lambda fails."
  default     = "myname@example.co.nz"
}

# Environment Variables to use in the lambda function
variable "VAULT_ADDR" {
  type        = string
  description = "Hashicorp Vault URL"
  default     = "http://127.0.0.1:8200"
}

variable "VAULT_NAMESPACE" {
  type        = string
  description = "Vault namespace where the aws auth method and the terraform secret engine are located."
  default     = "admin"
}

variable "VAULT_TFC_ROLE" {
  type        = string
  description = "Role to be used in the Terraform Secret Engine configurations."
  default     = "terraform-se-role"
}

variable "VAULT_AWS_ROLE" {
  type        = string
  description = "Role to be used to grant permissions after aws auth login."
  default     = "aws-auth-role"
}