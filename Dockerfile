FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量，避免 Python 输出缓冲
ENV PYTHONUNBUFFERED=1

# 安装系统构建工具，以应对需要编译的 Python 包
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先拷贝依赖清单并安装，充分利用 Docker 缓存
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 拷贝应用代码和训练好的模型
COPY app/ /app/app/
COPY ml/registry/ /app/ml/registry/

# 创建非 root 用户并切换，遵循最小权限原则
RUN useradd -m appuser
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]