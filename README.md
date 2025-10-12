# DBA 网站与简历生成

本仓库包含两部分：
- `web/`：DBA 技术与案例网站（Flask，容器化，部署到 Azure Container Apps）
- `resume/`：简历生成与 OCR 工具（ReportLab 生成 PDF，EasyOCR 从截图识别文本）

## 目录结构
- web/
  - app.py, templates/, static/, cases.json, Dockerfile, docker-compose.yml
- resume/
  - generate_cv_pdf.py, ocr_extract.py, dba_cv.txt, screenshot/, screenshots_ocr.*
- k8s/
  - dba-site.yaml（可选：K8S 部署清单）

## 开发与运行

- 网站本地运行
```bash
cd web
pip install -r requirements.txt
python app.py
# 浏览器访问 http://localhost:8080
```

- Docker 本地运行
```bash
cd web
docker build -t dba-site:latest .
docker run --rm -p 8080:8080 --name dba-site dba-site:latest
```

- 生成简历 PDF（输出在 resume/ 内）
```bash
pip install reportlab
python resume/generate_cv_pdf.py
```

> 网站使用的 PDF 位于 `web/static/`，构建镜像前确保该目录存在目标 PDF（默认文件名：刘力夫_DBA_简历_CN_v3.pdf）。

## 部署
- CI/CD：.github/workflows/deploy.yml（Push 到 main 或打 tag 会触发）
- 目标：Azure Container Apps（资源组：dba-site-rg，环境：dba-env，应用：dba-site）

更多细节参见：
- CI_CD_GUIDE.md（流水线与命令指南）
- AUDIT_LOG.md（完整审计日志）
