# DBA 站点容器化 CI/CD（GitHub Actions + Azure Container Apps）

本指南描述如何：
- 使用 Git 管理源码
- 通过 GitHub Actions 自动构建并推送镜像至 ACR
- 自动更新 Azure Container Apps（ACA）

## 一次性准备

1) Azure 资源已存在：
- 资源组：dba-site-rg（eastasia）
- ACR：lifudbaacr
- ACA 环境：dba-env
- ACA 应用：dba-site

2) 创建服务主体并授权（在本机终端运行）
```bash
SUB_ID="<你的订阅ID>"
az ad sp create-for-rbac \
  --name "gh-actions-dba-site" \
  --role "Contributor" \
  --scopes "/subscriptions/${SUB_ID}/resourceGroups/dba-site-rg" \
  --sdk-auth

# 赋予 ACR 推送权限
ACR_ID=$(az acr show -n lifudbaacr --query id -o tsv)
az role assignment create \
  --assignee "<上一步输出的 appId>" \
  --role "AcrPush" \
  --scope "$ACR_ID"
```
将 `az ad sp create-for-rbac --sdk-auth` 的 JSON 整段复制，稍后粘贴到 GitHub Secrets。

3) 在 GitHub 仓库添加 Secrets：
- AZURE_CREDENTIALS：上一步 JSON
- AZURE_CONTAINERAPPS_ENV：dba-env
- AZURE_RESOURCE_GROUP：dba-site-rg
- AZURE_CONTAINERAPP_NAME：dba-site
- AZURE_LOCATION：eastasia
- ACR_LOGIN_SERVER：lifudbaacr.azurecr.io

## 工作流文件
将 `.github/workflows/deploy.yml` 提交到仓库（已由我们创建）。

## 开发与发布
- feature/* 分支开发 → PR 合并 main 自动发布 latest
- 打 tag（如 v1.0.0）→ 自动发布版本标签镜像并部署

```bash
git checkout -b feature/x
# 修改 web/*
git add .
git commit -m "feat: x"
git push origin feature/x
# PR 合并 main 后

git checkout main
git pull
git tag -a v1.0.0 -m "release v1.0.0"
git push origin v1.0.0
```

## 回滚与流量切换（可选）
```bash
# 多修订模式
a z containerapp revision set-mode -n dba-site -g dba-site-rg --mode multiple
# 查看修订
a z containerapp revision list -n dba-site -g dba-site-rg -o table
# 切流量
a z containerapp ingress traffic set -n dba-site -g dba-site-rg \
  --revision-weight dba-site--<rev>=100
```

## 计费查看（CLI）
```bash
SUB_ID="<你的订阅ID>"
az costmanagement query \
  --type Usage \
  --scope /subscriptions/$SUB_ID/resourceGroups/dba-site-rg \
  --timeframe MonthToDate \
  --dataset-aggregation cost=sum \
  --dataset-grouping name=ResourceType \
  -o table
```
更多请参考 README 和工作流内注释。

