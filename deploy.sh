#!/bin/bash
set -e

SERVER="andr@192.168.0.188"
SSH_KEY="$HOME/.ssh/id_ed25519"
APP_DIR="/home/andr/d4tech"

echo "==> Копируем файлы на сервер..."
rsync -avz --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.production' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='staticfiles' \
  -e "ssh -i $SSH_KEY" \
  . "$SERVER:$APP_DIR"

echo "==> Копируем .env.production как .env на сервер..."
scp -i "$SSH_KEY" .env.production "$SERVER:$APP_DIR/.env"

echo "==> Запускаем docker compose на сервере..."
ssh -i "$SSH_KEY" "$SERVER" "cd $APP_DIR && docker compose pull 2>/dev/null || true && docker compose up -d --build"

echo "==> Деплой завершён."
