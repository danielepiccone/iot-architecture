terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.60.0"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

# Patched for localstack

provider "aws" {
  region = "us-east-1"

  access_key = "test"
  secret_key = "test"

  s3_force_path_style         = true
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    s3         = "http://localhost:4566"
    sts        = "http://localhost:4566"
    dynamodb   = "http://localhost:4566"
    lambda     = "http://localhost:4566"
    sqs        = "http://localhost:4566"
    sns        = "http://localhost:4566"
    cloudwatch = "http://localhost:4566"
    iam        = "http://localhost:4566"
  }
}
