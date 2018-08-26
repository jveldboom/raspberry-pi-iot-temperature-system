resource "aws_iot_policy" "policy" {
  name        = "temperature-system-policy"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "iot:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iot_thing_type" "type" {
  name = "temperature"
}