#!/bin/bash

# Останавливаем скрипт при любой ошибке
set -e

echo "--- 🛠️ СТАРТ СБОРКИ ОБРАЗА GENESIS v6.6.1 ---"
# Собираем актуальный образ
gcloud builds submit --tag gcr.io/genesis-psy-2026/genesis-app .

echo "--- 🚀 ДЕПЛОЙ В GOOGLE CLOUD RUN (FIX NEON SNI) ---"
# Деплоим с правильными параметрами для Neon и исправленным синтаксисом
gcloud run deploy genesis-new-live \
  --image gcr.io/genesis-psy-2026/genesis-app \
  --region europe-west4 \
  --set-env-vars "DATABASE_URL=postgresql://neondb_owner:npg_L7MysO6bSKpw@ep-damp-math-al92xna7-pooler.a2.eu-central-1.aws.neon.tech/neondb?sslmode=require&options=endpoint%3Dep-damp-math-al92xna7" \
  --allow-unauthenticated

echo "--- ✅ ГОТОВО! СИСТЕМА ОБНОВЛЕНА И БАЗА ПОДКЛЮЧЕНА ---"