# 部署指南 (Deployment Guide)

本项目已完全容器化。请确保宿主机安装了 Docker Desktop。

## 本地运行步骤
1. 构建 Docker 镜像：
   docker build -t rain-predictor:v1 .
2. 启动容器：
   docker run -d --name rain-app -p 8000:8000 rain-predictor:v1
3. 访问网页：打开浏览器输入 `http://localhost:8000`
