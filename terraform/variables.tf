variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "eastus"
}

variable "project_name" {
  description = "Short lowercase project name used in Azure resource names."
  type        = string
  default     = "agroindustria"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}

variable "postgres_admin_user" {
  description = "PostgreSQL administrator user."
  type        = string
  default     = "pgadmin"
}

variable "postgres_admin_password" {
  description = "PostgreSQL administrator password."
  type        = string
  sensitive   = true
}

variable "database_name" {
  description = "Application database name."
  type        = string
  default     = "agroindustria_dw"
}

variable "postgres_version" {
  description = "Azure PostgreSQL major version."
  type        = string
  default     = "16"
}

variable "sku_name" {
  description = "Azure PostgreSQL Flexible Server SKU."
  type        = string
  default     = "B_Standard_B1ms"
}

variable "storage_mb" {
  description = "PostgreSQL storage size in MB."
  type        = number
  default     = 32768
}

variable "allowed_ip_start" {
  description = "Firewall start IPv4 for automation access."
  type        = string
}

variable "allowed_ip_end" {
  description = "Firewall end IPv4 for automation access."
  type        = string
}
