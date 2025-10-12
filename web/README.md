# DBA 技术与案例网站

一个轻量级 Flask 网站，展示刘力夫的 DBA 技术方向与企业实际应用案例，支持 Docker/K8S 部署。

## 结构
- app.py / templates / static：Web 应用
- cases.json：案例数据
- Dockerfile / docker-compose.yml：容器化部署
- k8s/dba-site.yaml：K8S 部署清单（Deployment+Service）

## 本地运行（Python）
```bash
cd web
pip install -r requirements.txt
python app.py
# 浏览器访问 http://localhost:8080
```

## Docker 构建与运行
```bash
cd web
docker build -t dba-site:latest .
docker run --rm -p 8080:8080 --name dba-site dba-site:latest
# 健康检查
curl http://localhost:8080/healthz
```

> 如需在容器内提供 PDF，请先将项目根目录的“刘力夫_DBA_简历_CN_v3.pdf”复制到 `web/static/` 再构建：
> Windows: `copy ..\刘力夫_DBA_简历_CN_v3.pdf web\static\`

## Docker Compose
```bash
cd web
docker compose up --build
```

## K8S 部署（本地 kind 或云上集群）
```bash
# 先把镜像推送到可访问的镜像仓库，或在集群内构建
kubectl apply -f ../k8s/dba-site.yaml
# 通过端口转发访问
kubectl port-forward svc/dba-site 8080:80
# 浏览器访问 http://localhost:8080
```


> CI note: this README change triggers workflow.

