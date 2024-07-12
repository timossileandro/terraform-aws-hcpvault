resource "aws_iam_user" "vault" {
  name = "${var.env}-${var.application}-user-01"
}

resource "aws_iam_user_policy" "vault" {
  name = "${var.env}-${var.application}-policy-01"
  user = aws_iam_user.vault.name
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "iam:GetInstanceProfile",
          "iam:GetUser",
          "iam:ListRoles",
          "iam:GetRole"
        ],
        "Resource" : "*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "sts:AssumeRole"
        ],
        "Resource" : [
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${aws_iam_role.vault.name}"
        ]
      }
    ]
  })
}

resource "aws_iam_role" "vault" {
  name = "${var.env}-${var.application}-role-01"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "AWS" : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/${aws_iam_user.vault.name}"
        },
        "Action" : "sts:AssumeRole"
      },
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "vault" {
  name        = "${var.env}-${var.application}-policy-02"
  description = "Allow IAM Role to use SNS Topic for the lambda function destination."
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Action" : [
          "sns:*"
        ],
        "Effect" : "Allow",
        "Resource" : "*"
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface"
        ],
        "Resource" : "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "vault" {
  role       = aws_iam_role.vault.name
  policy_arn = aws_iam_policy.vault.arn
}