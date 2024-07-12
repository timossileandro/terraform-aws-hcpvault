resource "aws_cloudwatch_event_rule" "lambda_event_rule" {
  name                = "${var.env}-${var.application}-eventbridge-01"
  description         = "Execute lambda function at 00.00 AM every day"
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_event_rule.name
  target_id = "SendToLambda"
  arn       = module.aws_lambda.lambda_function_arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = module.aws_lambda.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_event_rule.arn
}