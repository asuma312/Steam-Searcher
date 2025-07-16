FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
WORKDIR /
COPY requirements.txt .
RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/frontend
RUN npm install

WORKDIR /

RUN chmod +x start.sh

EXPOSE 5000 5173
CMD ["./start.sh"]