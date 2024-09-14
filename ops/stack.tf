data "azurerm_client_config" "current" {}

resource "random_id" "unique-id" {
  byte_length = 1
}

resource "azurerm_resource_group" "af-rg" {
  name     = "af-rg-${var.env}"
  location = var.region
}
resource "azurerm_storage_account" "example-sa" {
  name                              = "examplesa${var.env}${random_id.unique-id.hex}"
  resource_group_name               = azurerm_resource_group.af-rg.name
  location                          = azurerm_resource_group.af-rg.location
  account_tier                      = "Standard"
  account_replication_type          = "LRS"
  min_tls_version                   = "TLS1_2"
  allow_nested_items_to_be_public   = false
  https_traffic_only_enabled        = true
  infrastructure_encryption_enabled = true
  public_network_access_enabled     = true

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

resource "azurerm_storage_container" "example" {
  name                 = "mycontainer"
  storage_account_name = azurerm_storage_account.example-sa.name
}

resource "azurerm_key_vault" "af-kv" {
  name                            = "af-kv-${var.env}${random_id.unique-id.hex}"
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
  enable_rbac_authorization       = true
  network_acls {
    default_action = "Deny"
    bypass         = "AzureServices"
  }
}

resource "azurerm_service_plan" "af-splan" {
  name                = "af-splan-${var.env}${random_id.unique-id.hex}"
  resource_group_name = azurerm_resource_group.af-rg.name
  location            = azurerm_resource_group.af-rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_application_insights" "af-appi" {
  name                = "af-appi-${var.env}${random_id.unique-id.hex}"
  location            = azurerm_resource_group.af-rg.location
  resource_group_name = azurerm_resource_group.af-rg.name
  application_type    = "web"
}

############################################
# AF V2
############################################
resource "azurerm_storage_account" "af-sa" {
  name                              = "afsa${var.env}${random_id.unique-id.hex}"
  resource_group_name               = azurerm_resource_group.af-rg.name
  location                          = azurerm_resource_group.af-rg.location
  account_tier                      = "Standard"
  account_replication_type          = "LRS"
  min_tls_version                   = "TLS1_2"
  allow_nested_items_to_be_public   = false
  https_traffic_only_enabled        = true
  infrastructure_encryption_enabled = true
  public_network_access_enabled     = true

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

resource "azurerm_linux_function_app" "af" {
  name                = "af-${var.env}${random_id.unique-id.hex}"
  resource_group_name = azurerm_resource_group.af-rg.name
  location            = azurerm_resource_group.af-rg.location

  storage_account_name          = azurerm_storage_account.af-sa.name
  storage_account_access_key    = azurerm_storage_account.af-sa.primary_access_key
  service_plan_id               = azurerm_service_plan.af-splan.id
  functions_extension_version   = var.function_version
  public_network_access_enabled = false
  https_only                    = true

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      python_version = var.python_version
    }
    application_insights_key = azurerm_application_insights.af-appi.instrumentation_key
  }
}


resource "azurerm_role_assignment" "function_storage_access" {
  scope                = azurerm_storage_account.af-sa.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.af.identity[0].principal_id
}
