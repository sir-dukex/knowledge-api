#!/usr/bin/env bash
set -e

# Git Bashのpaht変換防止
export MSYS_NO_PATHCONV=1

# .env.commonが存在するか確認
if [ -f ".env.common" ]; then
  source .env.common
else 
  echo ".env.common file does not exist."
  exit 1
fi

# azconfig.txt ファイルから環境変数を読み込む
source ./azconfig_$ENVIRONMENT.txt

# Image Nameを指定
MY_IMAGE_NAME="msm_${ENVIRONMENT}_im"

echo "Building image: $MY_IMAGE_NAME"

# ACRのログインサーバーを取得
loginServer=$(az acr show --name $acrName --resource-group $rgName --query "loginServer" --output tsv)

# ACRの管理ユーザー名とパスワードを取得
adminUser=$(az acr credential show --name $acrName --resource-group $rgName --query "username" --output tsv)
adminPassword=$(az acr credential show --name $acrName --resource-group $rgName --query "passwords[0].value" --output tsv)

# Dockerにログイン
echo "Logging into ACR..."
echo $adminPassword | docker login $loginServer -u $adminUser --password-stdin

# build
# MacのプロセッサがApple Siliconかどうかを判断
if [[ $(uname -m) == "arm64" ]]; then
    echo "Apple Silicon detected. Building for linux/amd64."
    # Apple Silicon用にビルド
    docker build -t $MY_IMAGE_NAME --platform linux/amd64 .
else
    echo "Not Apple Silicon. Building for the default platform."
    # 通常のプラットフォーム用にビルド
    docker build -t $MY_IMAGE_NAME .
fi

# Dockerイメージのタグ付け
echo "Tagging image..."
docker tag $MY_IMAGE_NAME:latest $loginServer/$MY_IMAGE_NAME:latest

# Dockerイメージをプッシュ
echo "Pushing image to ACR..."
docker push $loginServer/$MY_IMAGE_NAME:latest

# 完了メッセージ
echo "Image successfully pushed to ACR."