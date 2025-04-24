terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=4.0"  # このバージョン以降で resource_provider_registrations がサポートされています
    }
  }
}

# 既存のリソースグループを指定する変数
variable "subscription_id" {
  type        = string
  description = "サブスクリプションid"
}

variable "resource_group_name" {
  type        = string
  description = "既存の Azure Resource Group の名前"
}

variable "location" {
  type        = string
  default     = "japaneast"
  description = "Azure リージョン (例: japaneast, japanwest)"
}

# ACR情報 (例: ACRのログイン情報) - 実際にはKeyVault等で管理推奨
variable "acr_name" {
  type        = string
  description = "ACR 名 (例: mycontainerregistry)"
}
variable "acr_username" {
  type        = string
  description = "ACRのユーザ名"
}
variable "acr_password" {
  type        = string
  description = "ACRのパスワード or Token"
}

# provider設定
provider "azurerm" {
  features {}
  resource_provider_registrations = "none"
  subscription_id = var.subscription_id
}

variable "azure_sql_server" {
  type        = string
  description = "Azure SQL Server名 (例: your-server.database.windows.net)"
}
variable "azure_sql_database" {
  type        = string
  description = "Azure SQL Database名"
}
variable "azure_sql_user" {
  type        = string
  description = "Azure SQLユーザ名"
}
variable "azure_sql_password" {
  type        = string
  description = "Azure SQLパスワード"
}

# Log Analytics Workspace
variable "log_analytics_workspace_name" {
  type        = string
  description = "Log Analytics Workspace名"
  default     = "knowledge-logs"
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = var.log_analytics_workspace_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

# Premiumプラン(EP1) - カスタムコンテナは通常Premium or Dedicatedが必要
resource "azurerm_service_plan" "function_plan" {
  name                = "knowledge-plan"
  resource_group_name = var.resource_group_name
  location            = var.location

  sku_name = "EP1"  # Premium
  os_type  = "Linux"
}

resource "random_integer" "rand_suffix" {
  min = 10000
  max = 99999
}

resource "azurerm_storage_account" "storage" {
  name                     = "knowledgeacct${random_integer.rand_suffix.result}"
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_application_insights" "app_insights" {
  name                = "knowledge-insights"
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.log_analytics.id
}

resource "azurerm_linux_function_app" "my_func_app" {
  name                       = "knowledge-func"
  resource_group_name        = var.resource_group_name
  location                   = var.location
  service_plan_id            = azurerm_service_plan.function_plan.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      docker {
        registry_url = "https://${var.acr_name}.azurecr.io"
        image_name   = "knowledge-api-prod"
        image_tag    = "latest"
        registry_username = var.acr_username
        registry_password = var.acr_password
      }
    }
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"      = "custom"
    "FUNCTIONS_CUSTOMHANDLER_PORT"  = "8000"
    "WEBSITE_RUN_FROM_PACKAGE"      = "0"
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.app_insights.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.app_insights.connection_string
    "AZURE_SQL_SERVER"              = var.azure_sql_server
    "AZURE_SQL_DATABASE"            = var.azure_sql_database
    "AZURE_SQL_USER"                = var.azure_sql_user
    "AZURE_SQL_PASSWORD"            = var.azure_sql_password
  }
}
