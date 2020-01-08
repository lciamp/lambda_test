data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "waffle_checkin"
  output_path = "waffle_checkin.zip"
}

resource "aws_lambda_function" "waffle_checkin" {
  filename         = "${data.archive_file.lambda_zip.output_path}"
  function_name    = "waffle_checkin"
  timeout          = 60
  role             = "arn:aws:iam::200882202304:role/iam_for_lambda_tf"
  handler          = "waffle_checkin.lambda_handler"
  runtime          = "python3.7"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
}
