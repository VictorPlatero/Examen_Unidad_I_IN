output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "postgres_server_name" {
  value = azurerm_postgresql_flexible_server.this.name
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.this.fqdn
}

output "database_name" {
  value = azurerm_postgresql_flexible_server_database.this.name
}

output "postgres_admin_user" {
  value = var.postgres_admin_user
}
