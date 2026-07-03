#!/bin/bash
set -e

# === НАСТРОЙКИ ===
SERVER="macar@192.168.0.188"
SSH_KEY="$HOME/.ssh/id_ed25519"
APP_DIR="/home/macar/d4tech"
IMAGE_NAME="d4tech-web"          # должно совпадать с image в compose
TAR_FILE="d4tech-image.tar"

echo "==> 1. Сборка Docker-образа локально..."
docker build -t "$IMAGE_NAME" .

echo "==> 2. Сохраняем образ в архив $TAR_FILE..."
docker save -o "$TAR_FILE" "$IMAGE_NAME"

echo "==> 3. Копируем архив на сервер..."
scp -i "$SSH_KEY" "$TAR_FILE" "$SERVER:$APP_DIR/"

echo "==> 4. Загружаем образ на сервере..."
ssh -i "$SSH_KEY" "$SERVER" "cd $APP_DIR && docker load -i $TAR_FILE"

echo "==> 5. Копируем остальные файлы проекта (кроме .env и т.п.)..."
rsync -avz \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.production' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='staticfiles' \
  -e "ssh -i $SSH_KEY" \
  . "$SERVER:$APP_DIR"

echo "==> 6. Копируем .env.production как .env..."
scp -i "$SSH_KEY" .env.production "$SERVER:$APP_DIR/.env"

echo "==> 7. Запускаем контейнеры (без сборки) на сервере..."
ssh -i "$SSH_KEY" "$SERVER" "cd $APP_DIR && docker compose up -d"

echo "==> 8. Удаляем архив на сервере и локально..."
ssh -i "$SSH_KEY" "$SERVER" "rm -f $APP_DIR/$TAR_FILE"
rm -f "$TAR_FILE"

echo "==> Деплой с локальной сборкой завершён."