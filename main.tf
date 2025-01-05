locals {
  name               = "cyborg-coffeeshop"
  backend_source_dir = "${path.module}/backend/"
  output_dir         = "${path.cwd}/tmp/"

  tags = {
    Project = local.name
  }
}

terraform {
  cloud {

    organization = "cyborg-coffeehouse"

    workspaces {
      name = "dev"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
