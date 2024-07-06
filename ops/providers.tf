terraform {
  required_version = ">= 1.9.1"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.111.0"
    }
  }
  backend "azurerm" {
    resource_group_name = "deploy-rg"
  }
}
