terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.39.0"
    }
  }
  
  backend "s3" {
    bucket         = "kandidat-2030"
    key            = "kandidat-2030/terraform.tfstate"
    region         = "eu-west-1"
    encrypt        = true
    dynamodb_table = "terraform_locks"
  }
}