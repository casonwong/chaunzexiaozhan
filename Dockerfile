# 使用具体版本号的官方 Python 基础镜像
FROM python:3.9-slim

# 设置环境变量以确保 Python 输出直接被打印，不进行缓冲
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt /app/

# 安装应用程序依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码到工作目录
COPY . /app

# 暴露 Flask 默认端口 5000
EXPOSE 5000

# 执行启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]