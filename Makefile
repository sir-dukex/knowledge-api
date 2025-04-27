# Makefile

# 変数
COMPOSE_DEV = docker-compose
COMPOSE_PROD = docker-compose -f docker-compose.prod.yml
APP_DEV = knowledge-api
APP_PROD = knowledge-api-prod
ACR_NAME = acryakkibetadev02
RG_NAME = rg-yakki-beta-dev02

# デフォルトのターゲット
.PHONY: help
help:
	@echo "利用可能なコマンド:"
	@echo "  make setup         - 環境設定ファイルの準備"
	@echo "  make build         - 開発環境のビルド"
	@echo "  make build-prod    - 本番環境のビルド"
	@echo "  make up            - 開発環境の起動"
	@echo "  make up-prod       - 本番環境の起動"
	@echo "  make down          - 開発環境の停止"
	@echo "  make down-prod     - 本番環境の停止"
	@echo "  make restart       - 開発環境の再起動"
	@echo "  make restart-prod  - 本番環境の再起動"
	@echo "  make logs          - 開発環境のログ表示"
	@echo "  make logs-prod     - 本番環境のログ表示"
	@echo "  make test          - すべてのテストを実行"
	@echo "  make test-unit     - 単体テストを実行"
	@echo "  make test-int      - 統合テストを実行"
	@echo "  make coverage      - テストカバレッジの計測"
	@echo "  make lint          - コードの静的解析"
	@echo "  make format        - コードの自動フォーマット"
	@echo "  make shell         - アプリケーションコンテナのシェルを起動"
	@echo "  make shell-prod    - 本番アプリケーションコンテナのシェルを起動"
	@echo "  make clean         - 不要なファイルを削除"
	@echo "  make clean-all     - すべてのコンテナ、イメージ、ボリュームを削除"

# 環境設定
.PHONY: setup
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env && \
		echo "環境設定ファイル(.env)を作成しました。必要に応じて編集してください。"; \
	else \
		echo "環境設定ファイル(.env)はすでに存在します。"; \
	fi

# Azure CLIのログイン
.PHONY: login
login:
	bash scripts/switch_azure_subscription.sh

# Docker操作 - 開発環境
.PHONY: build up down restart logs shell
build:
	$(COMPOSE_DEV) build

up:
	$(COMPOSE_DEV) up -d

down:
	$(COMPOSE_DEV) down

restart:
	$(COMPOSE_DEV) restart

logs:
	$(COMPOSE_DEV) logs -f

shell:
	$(COMPOSE_DEV) exec $(APP_DEV) /bin/bash


# DB初期化
.PHONY: init-db
init-db:
	$(COMPOSE_DEV) exec $(APP_DEV) python -c "from app.infrastructure.database.connection import init_db; init_db()"


# Docker操作 - 本番環境
.PHONY: build-prod build-prod-amd64 build-prod-amd64-webapp up-prod down-prod restart-prod logs-prod shell-prod
build-prod:
	$(COMPOSE_PROD) build

# Apple Silicon用: amd64イメージを直接ビルド
build-prod-amd64:
	docker build --platform linux/amd64 -t $(APP_PROD) -f docker/app/Dockerfile.prod .

# Apple Silicon用: amd64イメージを直接ビルド (Webアプリ用)
build-prod-amd64:
	docker build --platform linux/amd64 -t $(APP_PROD) -f docker/app/Dockerfile.webapp .

up-prod:
	$(COMPOSE_PROD) up -d

down-prod:
	$(COMPOSE_PROD) down

restart-prod:
	$(COMPOSE_PROD) restart

logs-prod:
	$(COMPOSE_PROD) logs -f

shell-prod:
	$(COMPOSE_PROD) exec $(APP_PROD) /bin/bash


# Dockerイメージのビルドとプッシュ - 本番環境
.PHONY: build-prod acr-login push-prod
tag-prod:
	docker tag $(APP_PROD) $(ACR_NAME).azurecr.io/$(APP_PROD):latest

acr-login:
	@loginServer=$$(az acr show --name $(ACR_NAME) --resource-group $(RG_NAME) --query "loginServer" --output tsv); \
	adminUser=$$(az acr credential show --name $(ACR_NAME) --resource-group $(RG_NAME) --query "username" --output tsv); \
	adminPassword=$$(az acr credential show --name $(ACR_NAME) --resource-group $(RG_NAME) --query "passwords[0].value" --output tsv); \
	echo $$adminPassword | docker login $$loginServer -u $$adminUser --password-stdin

push-prod: tag-prod acr-login
	docker push $(ACR_NAME).azurecr.io/$(APP_PROD):latest

# テスト
.PHONY: test test-unit test-int coverage
test:
	$(COMPOSE_DEV) exec $(APP_DEV) pytest tests/

test-unit:
	$(COMPOSE_DEV) exec $(APP_DEV) pytest tests/unit/

test-int:
	$(COMPOSE_DEV) exec $(APP_DEV) pytest tests/integration/

coverage:
	$(COMPOSE_DEV) exec $(APP_DEV) pytest --cov=app --cov-report=term --cov-report=html tests/

# Alembicマイグレーション
.PHONY: alembic-init alembic-revision alembic-upgrade
alembic-init:
	$(COMPOSE_DEV) run --rm $(APP_DEV) alembic init migrations

alembic-revision:
	$(COMPOSE_DEV) run --rm $(APP_DEV) alembic revision --autogenerate -m "initial migration"

alembic-upgrade:
	$(COMPOSE_DEV) run --rm $(APP_DEV) alembic upgrade head
	

# コード品質
.PHONY: lint format
lint:
	$(COMPOSE_DEV) exec $(APP_DEV) flake8 app/ tests/

sorting:
	$(COMPOSE_DEV) exec $(APP_DEV) isort app/ tests/

format:
	$(COMPOSE_DEV) exec $(APP_DEV) black app/ tests/

# App Service環境変数一括登録
.PHONY: set-appservice-env
set-appservice-env:
	bash scripts/set_appservice_env.sh

# クリーンアップ
.PHONY: clean clean-all
clean:
	find . -name __pycache__ -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".coverage" -delete
	find . -name "coverage.xml" -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	find . -name "htmlcov" -type d -exec rm -rf {} +

clean-all: down down-prod
	docker system prune -af --volumes


# OpenAPIドキュメントの取得
.PHONY: openapi
openapi:
	curl -X GET "https://knowledge-func.azurewebsites.net/openapi.json" | jq . > openapi.json