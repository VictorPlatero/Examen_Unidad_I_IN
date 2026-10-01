resource "random_string" "suffix" {
  length  = 6
  lower   = true
  upper   = false
  numeric = true
  special = false
}

locals {
  name_prefix = "${var.project_name}-${var.environment}-${random_string.suffix.result}"
}

resource "azurerm_resource_group" "this" {
  name     = "rg-${local.name_prefix}"
  location = var.location
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = "psql-${local.name_prefix}"
  resource_group_name    = azurerm_resource_group.this.name
  location               = azurerm_resource_group.this.location
  version                = var.postgres_version
  administrator_login    = var.postgres_admin_user
  administrator_password = var.postgres_admin_password
  sku_name               = var.sku_name
  storage_mb             = var.storage_mb
  zone                   = "1"

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  public_network_access_enabled = true
}

resource "azurerm_postgresql_flexible_server_database" "this" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.this.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "github_runner" {
  name             = "github-actions-runner"
  server_id        = azurerm_postgresql_flexible_server.this.id
  start_ip_address = var.allowed_ip_start
  end_ip_address   = var.allowed_ip_end
}
