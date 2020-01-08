terraform {
  required_version = "0.11.11"
}

provider "aws" {
  version = "~> 2.2"
  region  = "us-east-1"
}
