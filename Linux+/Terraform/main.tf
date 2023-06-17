terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 1.16.0"
    }
  }
}

provider "linode" {
  token = ""
}

resource "linode_instance" "my_instance" {
  label  = "johnbox"
  image  = "linode/ubuntu18.04"
  region = "eu-west"
  type   = "g6-standard-2"

  root_pass = ""
}
