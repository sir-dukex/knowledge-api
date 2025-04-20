#!/bin/bash

# Usage: ./scripts/set_appservice_env.sh [.env file path (optional)]
# .envファイルからAPP_SERVICE_NAME, RESOURCE_GROUP, その他の環境変数を取得し、App Serviceに一括登録する

set -e

ENV_FILE="${1:-.env}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Env file '$ENV_FILE' not found."
  exit 1
fi

# .envからAPP_SERVICE_NAMEとRESOURCE_GROUPを取得
APP_SERVICE_NAME=$(grep '^APP_SERVICE_NAME=' "$ENV_FILE" | head -n1 | cut -d '=' -f2- | tr -d '"')
RESOURCE_GROUP=$(grep '^RESOURCE_GROUP=' "$ENV_FILE" | head -n1 | cut -d '=' -f2- | tr -d '"')

if [ -z "$APP_SERVICE_NAME" ] || [ -z "$RESOURCE_GROUP" ]; then
  echo "APP_SERVICE_NAMEまたはRESOURCE_GROUPが.envに定義されていません。"
  exit 1
fi

echo "Registering environment variables from $ENV_FILE to App Service: $APP_SERVICE_NAME (Resource Group: $RESOURCE_GROUP)"

# Prepare settings as JSON array (APP_SERVICE_NAME, RESOURCE_GROUPは除外)
SETTINGS=()
while IFS='=' read -r key value; do
  [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
  [[ "$key" == "APP_SERVICE_NAME" || "$key" == "RESOURCE_GROUP" ]] && continue
  value="${value%\"}"
  value="${value#\"}"
  SETTINGS+=("$key=$value")
done < <(grep -v '^#' "$ENV_FILE" | grep -v '^\s*$')

az webapp config appsettings set \
  --name "$APP_SERVICE_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --settings "${SETTINGS[@]}"

echo "Done."
