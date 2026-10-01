# Secretos requeridos

## GitHub Actions

| Nombre | Uso |
|---|---|
| AZURE_CREDENTIALS | JSON de service principal para `azure/login`. |
| POSTGRES_ADMIN_PASSWORD | Contrasena del administrador de PostgreSQL usada por Terraform. |
| AZURE_RESOURCE_GROUP | Grupo de recursos creado por Terraform, usado por `setup.yml`. |
| AZURE_POSTGRES_SERVER | Nombre del servidor PostgreSQL Flexible Server, usado por `setup.yml`. |
| DB_HOST | FQDN del servidor PostgreSQL. |
| DB_NAME | Base de datos, por defecto `agroindustria_dw`. |
| DB_USER | Usuario de PostgreSQL. |
| DB_PASSWORD | Contrasena de PostgreSQL. |
| POWERBI_TENANT_ID | Tenant ID de Microsoft Entra ID. |
| POWERBI_CLIENT_ID | Client ID del app registration con permisos Power BI. |
| POWERBI_CLIENT_SECRET | Client secret del app registration. |
| POWERBI_WORKSPACE_ID | Workspace destino del reporte. |

## Variables opcionales

| Nombre | Valor sugerido |
|---|---|
| AZURE_LOCATION | `eastus`, `brazilsouth` u otra region disponible para PostgreSQL Flexible Server. |
