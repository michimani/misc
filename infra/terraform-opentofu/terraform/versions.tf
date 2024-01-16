terraform {
  required_version = ">= 1.6.6"
  required_providers {
    aws = "= 5.32.1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}
