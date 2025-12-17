FROM python:3.12-slim
WORKDIR /app

# 安裝 sqlite3 指令列工具 (方便教學除錯)
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py db_init.py ./

# 初始化 SQLite 資料庫
RUN python db_init.py

EXPOSE 5000
CMD ["python", "app.py"]
