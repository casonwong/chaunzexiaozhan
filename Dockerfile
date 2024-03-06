# 基于官方 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 Python 依赖文件到容器中
COPY requirements.txt .

# 使用 pip 安装依赖，这里假设 gunicorn 也在 requirements.txt 中声明了
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . .

# 暴露容器监听的端口
EXPOSE 5000

# 设置环境变量，确保 python 输出直接打印到终端，不需要缓冲
ENV PYTHONUNBUFFERED 1

# 运行 Gunicorn，并绑定容器的 5000 端口
CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:5000", "app:app"]