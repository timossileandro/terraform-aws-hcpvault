data "aws_caller_identity" "current" {}

module "aws_lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "7.7.0"

  create_role = false
  lambda_role = aws_iam_role.vault.arn

  function_name      = "${var.env}-${var.application}-lambda-01"
  description        = "Function API Token rotation"
  authorization_type = "AWS_IAM"
  handler            = "lambda_handler.lambda_handler"
  runtime            = "python3.12"

  source_path = "./src"

  destination_on_failure = aws_sns_topic.vault_lambda_email.arn
  destination_on_success = aws_sns_topic.vault_lambda_message.arn

  layers = ["arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python312:8"]

  timeout = 60

  environment_variables = {
    VAULT_ADDR       = var.VAULT_ADDR
    VAULT_NAMESPACE  = var.VAULT_NAMESPACE
    VAULT_TFC_ROLE   = var.VAULT_TFC_ROLE
    VAULT_AWS_ROLE   = var.VAULT_AWS_ROLE
    DEST_SNS_FAILURE = aws_sns_topic.vault_lambda_email.arn
    DEST_SNS_SUCCESS = aws_sns_topic.vault_lambda_message.arn
  }

  depends_on = [aws_sns_topic.vault_lambda_email, aws_sns_topic.vault_lambda_message]
}