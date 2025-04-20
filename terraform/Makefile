# Makefile

.PHONY: init plan apply destroy

## 初期化: terraform init
init:
	terraform init -upgrade

## 設計確認: terraform plan
plan:
	terraform plan -var-file="terraform.tfvars"

## 適用: terraform apply
apply:
	terraform apply -auto-approve -var-file="terraform.tfvars"

## 削除: terraform destroy
destroy:
	terraform destroy -auto-approve -var-file="terraform.tfvars"
