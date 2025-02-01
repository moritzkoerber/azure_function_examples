terraform {
  required_version = ">= 0.1"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.17"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
  backend "azurerm" {
    resource_group_name  = "terraform-rg"
    storage_account_name = "generaltfstatesta"
    container_name       = "af-tf-state"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}
