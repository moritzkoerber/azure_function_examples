
resource "azurerm_resource_group" "rg" {
  name     = "af-rg-${var.region}-${var.env}"
  location = var.region
}

resource "azurerm_storage_account" "sa" {
  name                            = "afsa${var.region}${var.env}"
  resource_group_name             = azurerm_resource_group.rg.name
  location                        = azurerm_resource_group.rg.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  public_network_access_enabled   = "false"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = "false"
  shared_access_key_enabled       = "false"
  blob_properties {
    delete_retention_policy {
      days = 7
    }
  }
}
