# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
GENESIS HR® // OMNIFACTORY EVO 

GEN-OS Platform / Supervisor Core

FILE: launcher.py
BUILD: 0099 [SUPERVISOR ENGAGED]
DESCRIPTION:
Главная точка входа платформы и супервизора кластера.
Принудительно выравнивает системное окружение (SQLite3/ChromaDB).
Проверяет сетевую инфраструктуру и порты.
Запускает асинхронное ядро Kernel (FastAPI) и разворачивает контракты API.

═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import socket
import logging
from datetime import datetime
from genesis.kernel.bootstrap import boot

# ==============================================================================
# СВЕРХРАННИЙ ХАК ОКРУЖЕНИЯ (Защита ChromaDB от старых версий SQLite3 на Windows)
# ==============================================================================
try:
    import sqlite3
    sqlite3.sqlite_version_info = (3, 35, 0)
except Exception:
    pass

# Настройка кастомного форматирования логов супервизора
class OmniFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        return f"[{timestamp}] [{record.levelname}] {record.getMessage()}"

logger = logging.getLogger("OmniSupervisor")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(OmniFormatter())
    logger.addHandler(handler)

# ==============================================================================
# СЕТЕВОЙ СУПЕРВИЗОР
# ==============================================================================
def check_port(port: int) -> bool:
    """Проверяет локальный порт на доступность перед стартом ядра."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) != 0

# ==============================================================================
# КИБЕР-БАННЕР СИСТЕМЫ
# ==============================================================================
def banner(port: int):
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                              ║")
    print("║                  ██████╗ ███████╗███╗   ██╗███████╗███████╗                  ║")
    print("║                 ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝                  ║")
    print("║                 ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗                  ║")
    print("║                 ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║                  ║")
    print("║                 ╚██████╔╝███████╗██║ ╚████║███████╗███████║                  ║")
    print("║                  ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝                  ║")
    print("║                                                                              ║")
    print("║                          G E N E S I S   H R  ®                              ║")
    print("║               OMNIFACTORY EVO // SYSTEM AUTOMATION KERNEL                  ║")
    print("║──────────────────────────────────────────────────────────────────────────────║")
    print("║ MODULE    : Application Launcher & Cluster Supervisor                        ║")
    print(f"║ STATUS    : STANDBY -> ACTIVATING [PORT {port} ALIGNED]                       ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

# ==============================================================================
# ТОЧКА ИНИЦИАЛИЗАЦИИ И ЗАПУСКА КЛАТЕРА
# ==============================================================================
def start():
    TARGET_PORT = 8089

    # 1. Отрисовка баннера
    banner(TARGET_PORT)

    # 2. Тестирование инфраструктуры
    logger.info("🔍 [SUPERVISOR] Запуск глубокой трассировки ядра...")

    # Защищаем хак версии: если он уже применен, не трогаем его повторно
    try:
        import sqlite3
        if sqlite3.sqlite_version_info < (3, 35, 0):
            sqlite3.sqlite_version_info = (3, 35, 0)
            logger.info("🗄️  [STATUS] SQLite3 успешно форсирован до 3.35.0")
    except Exception as e:
        logger.warning(f"⚠️  Не удалось применить хак SQLite3: {e}")

    # Проверка порта
    if not check_port(TARGET_PORT):
        logger.error(f"🚨 [STATUS] Сетевой порт ядра {TARGET_PORT}: ЗАНЯТ!")
        logger.info("⚡ Рекомендация: Выполните 'taskkill /F /IM python.exe' в терминале.")
        sys.exit(1)
    else:
        logger.info(f"📡 [STATUS] Сетевой порт ядра {TARGET_PORT}: СВОБОДЕН")

    # --- ВОТ ЗДЕСЬ МЫ СТАВИМ ЛОВУШКУ ДЛЯ МОЛЧАЛИВОГО КРАША ---
    logger.info("⏳ [TRACE] Вход в точку инициализации boot()...")
    try:
        kernel = boot()
        logger.info("✓ [TRACE] boot() успешно выполнен. Ядро в памяти.")
    except BaseException as e:
        # Использование BaseException перехватит даже системные выходы sys.exit()
        logger.critical(f"❌ Критический сбой внутри genesis.kernel.bootstrap.boot: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 4. Вывод системных параметров загруженного ядра
    print("════════════════════════════════════════════════════════════")
    print(" PLATFORM STATUS")
    print("════════════════════════════════════════════════════════════")
    # Используем безопасные get-методы, чтобы не упасть, если атрибуты отсутствуют
    print(f"Core Engine ......... {getattr(kernel, 'ENGINE_NAME', 'OmniFactory Enterprise Runtime')}")
    print(f"Version ............. {getattr(kernel, 'VERSION', 'Unknown')}")
    print(f"Platform ............ {getattr(kernel, 'PLATFORM', 'GEN-OS Engine')}")
    print(f"Supervisor Base ..... GEN-OS Cluster Manager v2")
    print(f"Timestamp (UTC) ..... {datetime.utcnow()}")
    print("════════════════════════════════════════════════════════════")
    print()

    # 5. Вывод загруженных модулей с проверкой наличия менеджера модулей
    print("════════════════════════════════════════════════════════════")
    print(" SYSTEM FUNCTIONAL MODULES")
    print("════════════════════════════════════════════════════════════")
    if hasattr(kernel, 'modules') and hasattr(kernel.modules, 'modules'):
        modules_list = kernel.modules.modules()
        for module in modules_list:
            state = "🟢 ONLINE" if getattr(module, 'enabled', False) else "🔴 OFFLINE"
            print(f" 🧬 [{state}] -> {getattr(module, 'title', 'Без названия'):<35}")
        print(f"\n[INFO] Реестр инициализирован. Модулей: {len(modules_list)}")
    else:
        print("  [WARN] Менеджер модулей ядра не обнаружен или пуст.")
    print("════════════════════════════════════════════════════════════")
    print()

    return kernel
