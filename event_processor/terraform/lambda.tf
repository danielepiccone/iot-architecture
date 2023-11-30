locals {
  lambda_name = "event_processor"
  sqs_queue   = "telemetry.fifo"
  handler     = "event_processor/lambda.lambda_handler"
}

# The queue is provisioned in the core layer
data "aws_sqs_queue" "telemetry" {
  name = local.sqs_queue
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "/tmp/lambda_function.zip"
  source_dir  = "../dist"
  excludes    = ["terraform"]
}

resource "aws_iam_role" "default" {
  name = local.lambda_name

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": "AllowAssumeRoleLambda"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "allow_lambda_execution" {
  role       = aws_iam_role.default.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "allow_sqs" {
  role       = aws_iam_role.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}

resource "aws_iam_role_policy_attachment" "allow_sns" {
  role       = aws_iam_role.default.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}



resource "aws_lambda_function" "default" {
  function_name = local.lambda_name
  runtime       = "python3.8"
  handler       = local.handler
  timeout       = 60
  memory_size   = 128

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = filebase64sha256(data.archive_file.lambda_zip.output_path)

  role = aws_iam_role.default.arn
}


resource "aws_lambda_event_source_mapping" "my_mapping" {
  event_source_arn  = data.aws_sqs_queue.telemetry.arn
  function_name     = aws_lambda_function.default.function_name
  batch_size        = 10
  starting_position = "LATEST"
}

resource "aws_lambda_permission" "allow_sqs_invoke" {
  statement_id  = "AllowExecutionFromSQS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.default.function_name
  principal     = "sqs.amazonaws.com"
  source_arn    = data.aws_sqs_queue.telemetry.arn
}
