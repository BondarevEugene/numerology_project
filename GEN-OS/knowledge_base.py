# ==============================================================================
# PROJECT: OMNIFACTORY EVO // COGNITIVE KNOWLEDGE POOL (ChromaDB)
# LOCATION: /knowledge_base.py
# ==============================================================================

import os
import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "chroma_db_storage")


def init_knowledge_base():
    """Инициализация базы и наполнение инженерным контекстом"""
    # Инициализируем локальный persistent-клиент ChromaDB (пишет данные на диск)
    client = chromadb.PersistentClient(path=DB_PATH)

    # Создаем или подключаем коллекцию воспоминаний
    collection = client.get_or_create_collection(name="omnifactory_intelligence")

    # Реальные системные данные и контекст твоей платформы для инжекции
    knowledge_data = [
        {
            "id": "doc_001",
            "text": "Платформа OmniFactory Evo создана инженером Бондаревым Е. в 2026 году. Архитектура построена на асинхронном FastAPI бэкенде (порт 8089) и фронтенде на Vite + React (порт 5173). Ядро управляет WSL2 ресурсами, Docker-контейнерами сборщиков и компиляцией когнитивных графов.",
        },
        {
            "id": "doc_002",
            "text": "В платформу интегрирован проект 'Genesys' — портал нумерологии и личностного развития. Он использует расчеты Психоматрицы (Пифагорейский квадрат) для генерации детальных PDF-отчетов и анализа потенциала пользователей с помощью AI-агентов.",
        },
        {
            "id": "doc_003",
            "text": "Встроенный конструктор ботов (IDE Builder Pro v8.0) использует библиотеку Drawflow для визуального проектирования логических цепочек. Доступные ноды: Webhook Шлюз, Celery Cron, Telegram Event, OpenAI Ядро, ChromaDB Нода и Python Скрипт.",
        }
    ]

    # Извлекаем тексты и ID
    documents = [item["text"] for item in knowledge_data]
    ids = [item["id"] for item in knowledge_data]

    # Добавляем в векторную базу. ChromaDB сама под капотом векторизует текст по дефолтной модели
    collection.upsert(
        documents=documents,
        ids=ids
    )
    print(f"◈ [SUCCESS] Векторная база ChromaDB успешно инициализирована по пути: {DB_PATH}")
    print(f"◈ [INFO] Инжектировано базовых когнитивных документов: {len(documents)}")


if __name__ == "__main__":
    init_knowledge_base()