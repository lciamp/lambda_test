data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "waffle_checkin"
  output_path = "waffle_checkin.zip"
}

resource "aws_lambda_function" "waffle_checkin" {
  filename         = "${data.archive_file.lambda_zip.output_path}"
  function_name    = "waffle_checkin"
  timeout          = 60
  role             = "${aws_iam_role.iam_for_lambda_tf.arn}"
  handler          = "waffle_checkin.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
}

resource "aws_iam_role" "iam_for_lambda_tf" {
  name = "iam_for_lambda_tf"

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
      "Sid": ""
    }
  ]
}
EOF
}
