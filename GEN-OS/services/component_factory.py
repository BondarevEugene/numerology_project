# ==============================================================================
# PROJECT: OMNIFACTORY EVO // SYSTEM NODE: BOT COMPONENT FACTORY
# REVISION: v1.0.0 // GEN-oS RUNTIME COMPLIANCE SPECIFICATION
# LOCATION: /services/component_factory.py
# PURPOSE: Canonical mapping of visual UI canvas elements into raw executable Python/Aiogram 3.x code
# ==============================================================================

from __future__ import annotations
import json
from typing import Dict, Any, List


class BotComponentLibrary:
    """
    Глобальный реестр и генератор фактических компонентов для Робостроителя.
    Переводит JSON-ноды холста в боевой асинхронный Python код.
    """

    def __init__(self):
        # Определение манифеста визуальных нод для Drawflow
        self.registry = {
            "text_message": {
                "name": "Текстовый ответ бота",
                "template": "await message.answer('{text}', parse_mode='Markdown')"
            },
            "inline_keyboard": {
                "name": "Инлайн Клавиатура (Кнопки)",
                "template": (
                    "builder = InlineKeyboardBuilder()\n"
                    "for btn in {buttons}:\n"
                    "    builder.button(text=btn['text'], callback_data=btn['callback'])\n"
                    "await message.answer('{text}', reply_markup=builder.as_markup())"
                )
            },
            "ai_inference": {
                "name": "Нейросетевая нода (Ollama)",
                "template": (
                    "ai_response = await asyncio.get_event_loop().run_in_executor(\n"
                    "    None, lambda: ollama.chat(model='{model}', messages=[{{'role': 'user', 'content': {context}}}])\n"
                    ")\n"
                    "await message.answer(ai_response['message']['content'])"
                )
            },
            "ecommerce_cart": {
                "name": "Модуль умной корзины",
                "template": (
                    "from brain.store_logic import EnterpriseStore\n"
                    "store = EnterpriseStore()\n"
                    "cart_text = store.add_to_cart(message.from_user.id, '{item_id}')\n"
                    "await message.answer(cart_text)"
                )
            }
        }

    # ------------------------------------------------------------

    def compile_node(self, node_type: str, data: Dict[str, Any]) -> str:
        """
        Компиляция отдельного графического компонента в исполняемый блок кода.
        """
        component = self.registry.get(node_type)
        if not component:
            return f"# ⚠️ Компонент [{node_type}] не зарегистрирован в ядре библиотеки"

        try:
            if node_type == "text_message":
                return component["template"].format(text=data.get("text", "Привет от OmniFactory!"))

            elif node_type == "inline_keyboard":
                # Форматируем JSON-строку кнопок в питоновский список
                btns = data.get("buttons", [{"text": "Купить Ноду", "callback": "buy_node"}])
                return component["template"].format(buttons=repr(btns), text=data.get("text", "Выберите действие:"))

            elif node_type == "ai_inference":
                model = data.get("model", "codellama")
                context = data.get("context", "message.text")
                return component["template"].format(model=model, context=context)

            elif node_type == "ecommerce_cart":
                return component["template"].format(item_id=data.get("item_id", "node_01"))

        except Exception as e:
            return f"# ❌ Критическая ошибка компиляции компонента {node_type}: {str(e)}"

        return ""

    # ------------------------------------------------------------

    def compile_canvas_flow(self, drawflow_export: Dict[str, Any]) -> str:
        """
        Полная потоковая сборка всей цепочки связей Drawflow в единый Python-файл.
        """
        python_handler_body = []

        # Парсим экспорт Drawflow (структура drawflow -> Home -> data)
        home_module = drawflow_export.get("drawflow", {}).get("Home", {})
        nodes = home_module.get("data", {})

        if not nodes:
            return "# ⚙️ Холст пуст. Сгенерирован дефолтный эхо-обработчик."

        for node_id, node_meta in nodes.items():
            node_type = node_meta.get("name")
            node_data = node_meta.get("data", {})

            compiled_block = self.compile_node(node_type, node_data)
            python_handler_body.append(f"    # --- NODE ID: {node_id} ({node_type}) ---")

            # Добавляем правильные PEP-8 отступы для асинхронной функции
            for line in compiled_block.split("\n"):
                python_handler_body.append(f"    {line}")
            python_handler_body.append("")

        return "\n".join(python_handler_body)

    # ------------------------------------------------------------

    def __repr__(self):
        return f"<BotComponentLibrary: {len(self.registry)} канонических компонентов>"


# Инициализация глобального синглтона для бэкенда FastAPI
component_library = BotComponentLibrary()
