# 审计日志（Azure Container Apps 部署与流水线搭建）

本日志用于完整记录从本地容器构建、Azure 资源创建、部署到 ACA，以至于 CI/CD 工作流配置的所有关键命令与结果，便于后续审计与学习复盘。

时间以本地执行为准，省略部分冗长输出，仅保留关键信息。

---

## 一、Docker 本地构建与运行（初次验证）
- docker --version
- docker build -t dba-site:latest .
- docker run --rm -d -p 8080:8080 --name dba-site dba-site:latest
- curl http://localhost:8080/healthz → ok
- 注入 PDF（免重建镜像）：
  - docker cp ..\刘力夫_DBA_简历_CN_v3.pdf dba-site:/app/static/刘力夫_DBA_简历_CN_v3.pdf

## 二、Azure CLI 安装与订阅/云环境
- 安装 Azure CLI（Windows）
- 使用完整路径调用 az：
  - "C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd" --version
- 设置云环境：
  - az cloud set -n AzureCloud
- 登录：
  - az login 或 az login --use-device-code
- 订阅确认：
  - az account show --query "{subscription:id, name:name}" -o json
  - 返回：{"name": "Azure subscription 1", "subscription": "f4bf506f-24a9-4886-a7e6-2f95ddc48db9"}

## 三、Provider 注册
- az provider register --namespace Microsoft.ContainerRegistry
- az provider register --namespace Microsoft.App
- az provider register --namespace Microsoft.OperationalInsights
- 轮询状态：
  - az provider show -n Microsoft.ContainerRegistry --query registrationState -o tsv → Registered
  - az provider show -n Microsoft.App --query registrationState -o tsv → Registered
  - az provider show -n Microsoft.OperationalInsights --query registrationState -o tsv → Registered

## 四、Azure 资源创建
- 资源组（已存在/确认）：
  - az group create -n dba-site-rg -l eastasia → Succeeded
- ACR 创建：
  - az acr create -n lifudbaacr -g dba-site-rg --sku Basic → Succeeded
  - loginServer：lifudbaacr.azurecr.io
- ACR 管理员启用（后续可关闭提高安全性）：
  - az acr update -n lifudbaacr --admin-enabled true

## 五、推送镜像到 ACR
- 本地镜像标记：
  - docker tag dba-site:latest lifudbaacr.azurecr.io/dba-site:latest
- 登录 ACR：
  - az acr login -n lifudbaacr → Login Succeeded
- 推送：
  - docker push lifudbaacr.azurecr.io/dba-site:latest → digest: sha256:7139c7... size: 2614

## 六、创建 ACA 环境与应用
- 创建 Container Apps 环境（自动创建 Log Analytics 工作区）：
  - az containerapp env create -n dba-env -g dba-site-rg -l eastasia → Succeeded
  - defaultDomain: kindglacier-68cfa4a8.eastasia.azurecontainerapps.io
- 创建 Container App（外网入口 8080）：
  - az containerapp create \
    -n dba-site -g dba-site-rg \
    --environment dba-env \
    --image lifudbaacr.azurecr.io/dba-site:latest \
    --ingress external --target-port 8080 \
    --registry-server lifudbaacr.azurecr.io \
    --registry-username lifudbaacr \
    --registry-password <已生成> \
    --min-replicas 1 --max-replicas 2 → Succeeded
- 获取访问域名：
  - az containerapp show -n dba-site -g dba-site-rg --query properties.configuration.ingress.fqdn -o tsv
  - 返回：dba-site.kindglacier-68cfa4a8.eastasia.azurecontainerapps.io
- 健康验证：
  - curl https://dba-site.kindglacier-68cfa4a8.eastasia.azurecontainerapps.io/healthz → ok

## 七、CI/CD：GitHub Actions 工作流
- 创建工作流文件：.github/workflows/deploy.yml
- 核心步骤：
  1) azure/login（服务主体）
  2) docker build/tag/push（到 lifudbaacr）
  3) az containerapp update（滚动更新镜像）
- 触发：push main、push tag v*.*.*

## 八、服务主体与 GitHub Secrets（建议）
- 创建服务主体并授予权限：
  - az ad sp create-for-rbac --name "gh-actions-dba-site" --role "Contributor" --scopes "/subscriptions/<SUB_ID>/resourceGroups/dba-site-rg" --sdk-auth
  - ACR 推送权限：
    - ACR_ID=$(az acr show -n lifudbaacr --query id -o tsv)
    - az role assignment create --assignee <appId> --role AcrPush --scope $ACR_ID
- 在 GitHub 仓库添加 Secrets：
  - AZURE_CREDENTIALS（上述 JSON 全量）
  - AZURE_CONTAINERAPPS_ENV=dba-env
  - AZURE_RESOURCE_GROUP=dba-site-rg
  - AZURE_CONTAINERAPP_NAME=dba-site
  - AZURE_LOCATION=eastasia
  - ACR_LOGIN_SERVER=lifudbaacr.azurecr.io

## 九、计费查询（命令行尝试与结论）
- 消费用量（预览命令，初期常返回空）：
  - az consumption usage list --start-date 2025-10-01 --end-date 2025-10-12 --top 50 -o json → []
- CostManagement 扩展：
  - az extension add --name costmanagement
  - az costmanagement query ...（部分环境下子命令不可用/数据延迟）
- REST API（Cost Management）：
  - az rest POST https://management.azure.com/.../providers/Microsoft.CostManagement/query?api-version=2023-08-01 （初期返回 Dataset invalid，常见于数据尚未出账或权限/配置差异）

结论：新创建资源的成本数据通常有 8–24 小时延迟。建议稍后再次运行命令，或在门户 Cost Management + Billing → Cost analysis 以资源组维度查看更直观。

## 十、后续优化建议
- 关闭 ACR 管理员账户，改用工作负载联邦/OIDC 登录
- ACA 多修订模式 + 灰度流量切换，支持快速回滚
- 镜像体积优化（多阶段构建、slim 基像）
- 日志留存策略与告警（Log Analytics 保留期与查询）

---

如需补充更精细的时间戳与完整输出，可在未来执行时把 az/dockers 命令前加 `PowerShell Start-Transcript` 启动全量审计输出并保存到 logs/ 目录。


## 十一、GitHub Secrets 配置（通过 GitHub CLI）
- 时间：本地执行，使用 gh CLI 登录并为仓库 liulifu/dba-site 写入 Secrets
- gh 版本：gh version 2.81.0
- 登录状态：gh auth status → account liulifu, scopes: repo, workflow, admin:repo_hook, write:packages
- 命令与结果（关键信息）：
  - gh repo set-default liulifu/dba-site → OK
  - Set AZURE_CREDENTIALS（从本地 sp_credentials.json 读取）：OK
  - Set AZURE_CONTAINERAPPS_ENV=dba-env：OK
  - Set AZURE_RESOURCE_GROUP=dba-site-rg：OK
  - Set AZURE_CONTAINERAPP_NAME=dba-site：OK
  - Set AZURE_LOCATION=eastasia：OK
  - Set ACR_LOGIN_SERVER=lifudbaacr.azurecr.io：OK
- 说明：AZURE_CREDENTIALS 为服务主体 JSON（仅写入 GitHub Secrets，未提交到 Git）
