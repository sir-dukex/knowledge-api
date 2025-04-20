#!/bin/bash
set -e

# Git Bashのpaht変換防止
export MSYS_NO_PATHCONV=1

# Azure CLI でログイン状態を確認
login_check=$(az account show 2>/dev/null)

if [ -z "$login_check" ]; then
    echo "You are not logged in. Please log in."
    az login
else
    echo "You are already logged in."
fi

# 選択可能なsubscriptionの表示
subscriptions=$(az account list --query '[].{name:name, id:id}' -o tsv)
echo "Subscriptions:"
echo "$subscriptions" | awk -F'\t' '{print NR ". " $1 " (" $2 ")"}'

# subscriptionの選択
read -p "Enter the number of the subscription you want to use: " subscription_number

# subscriptionを設定
subscription_id=$(echo "$subscriptions" | awk -F'\t' -v subscription_number="$subscription_number" 'NR==subscription_number {print $2}')
az account set --subscription "$subscription_id"
echo "Subscription set to $subscription_id"