provider "aws" {
  region = "us-east-2"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

locals {
  prefix       = "drums-practice-logs"
  django_image = "drums_practice_logs"
  proxy_image  = "nginx"
}