terraform {
  required_version = ">= 0.1"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.111.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "deploy-rg"
    storage_account_name = "generaltfstatesta"
    container_name       = "tf-state"
    key                  = "terraform.tfstate"
  }
}
