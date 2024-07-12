resource "aws_sns_topic" "vault_lambda_message" {
  name = "${var.env}-${var.application}-snstopic-01"
}

resource "aws_sns_topic" "vault_lambda_email" {
  name = "${var.env}-${var.application}-snstopic-02"
}

resource "aws_sns_topic_subscription" "sns_sub_message" {
  topic_arn = aws_sns_topic.vault_lambda_message.arn
  protocol  = "lambda"
  endpoint  = module.aws_lambda.lambda_function_arn
}

resource "aws_sns_topic_subscription" "sns_sub_email" {
  topic_arn = aws_sns_topic.vault_lambda_email.arn
  protocol  = "email"
  endpoint  = var.sns_email
} 