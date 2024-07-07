
resource "azurerm_resource_group" "af-rg" {
  name     = "af-rg-${var.env}"
  location = var.region
}

resource "azurerm_storage_account" "af-sa" {
  name                              = "afsa${var.env}"
  resource_group_name               = azurerm_resource_group.af-rg.name
  location                          = azurerm_resource_group.af-rg.location
  account_tier                      = "Standard"
  account_replication_type          = "LRS"
  min_tls_version                   = "TLS1_2"
  allow_nested_items_to_be_public   = false
  enable_https_traffic_only         = true
  infrastructure_encryption_enabled = true
  public_network_access_enabled     = false

  sas_policy {
    expiration_period = "90.00:00:00"
    expiration_action = "Log"
  }

  blob_properties {
    delete_retention_policy {
      days = 7
    }
  }
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "af-kv" {
  name                            = "afkv${var.env}"
  location                        = azurerm_resource_group.af-rg.location
  resource_group_name             = azurerm_resource_group.af-rg.name
  tenant_id                       = data.azurerm_client_config.current.tenant_id
  sku_name                        = "standard"
  enabled_for_disk_encryption     = true
  enabled_for_deployment          = true
  enabled_for_template_deployment = true
  purge_protection_enabled        = true
  soft_delete_retention_days      = 30
  public_network_access_enabled   = false
  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }
}
