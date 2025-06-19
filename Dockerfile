FROM python:3.10-slim

# 環境変数（任意で変更可能）
ENV DD_SERVICE=demo-apm-python \
    DD_ENV=demo \
    DD_VERSION=1.0 \
    DD_TRACE_ENABLED=true \
    DD_LOGS_INJECTION=true \
    DD_RUNTIME_METRICS_ENABLED=true

WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードをコピー
COPY app.py .

# ポートを公開
EXPOSE 5000

# ddtrace-run でアプリを起動
CMD ["ddtrace-run", "python", "app.py"]

