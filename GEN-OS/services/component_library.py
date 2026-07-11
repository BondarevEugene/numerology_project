import json
import logging

logger = logging.getLogger("ComponentLibrary")


class ComponentLibrary:
    def __init__(self):
        pass

    def compile_canvas_flow(self, raw_data: dict) -> str:
        """
        Парсит структуру Drawflow и собирает тело для функции core_canvas_router
        """
        # Безопасно извлекаем ноды из структуры Drawflow
        # Обычно структура выглядит так: payload['drawflow']['Home']['data']
        drawflow_pages = raw_data.get("drawflow", {})
        nodes = {}

        for page in drawflow_pages.values():
            nodes.update(page.get("data", {}))

        if not nodes:
            logger.warning("🚸 Холст пуст или структура Drawflow неверна.")
            return "    # Холст был пуст\n    pass"

        code_lines = []
        code_lines.append("    # Автогенерированный конвейер обработки OmniFactory")
        code_lines.append("    user_text = message.text\n")

        # Ищем стартовую ноду (например, команду /start или текстовый триггер)
        # Для примера сгенерируем базовую логику эха и проверку нод:
        has_ai_node = any(node.get("name") == "ollama_ai" for node in nodes.values())

        # Перебираем ноды и генерируем их логику
        for node_id, node_data in nodes.items():
            node_name = node_data.get("name")
            data_vars = node_data.get("data", {})

            code_lines.append(f"    # Блок: {node_name} (ID: {node_id})")

            if node_name == "telegram_reply":
                reply_text = data_vars.get("text", "Привет от OmniFactory!")
                code_lines.append(f"    if user_text == '/start':")
                code_lines.append(f"        await message.answer('{reply_text}')")
                code_lines.append(f"        return")

            elif node_name == "ollama_ai":
                model_name = data_vars.get("model", "llama3")
                system_prompt = data_vars.get("system", "You are a helpful assistant")

                code_lines.append("    # Вызов локального ИИ-компонента")
                code_lines.append("    try:")
                code_lines.append(f"        response = ollama.chat(model='{model_name}', messages=[")
                code_lines.append(f"            {{'role': 'system', 'content': '{system_prompt}'}},")
                code_lines.append("            {'role': 'user', 'content': user_text}")
                code_lines.append("        ])")
                code_lines.append("        await message.answer(response['message']['content'])")
                code_lines.append("    except Exception as ai_err:")
                code_lines.append(f"        await message.answer(f'Ошибка ИИ: {{ai_err}}')")

        # Если нод не обнаружено или они не подошли
        code_lines.append("\n    await message.answer('Кнопка или команда не распознана backend-движком.')")

        # Выравниваем отступами (4 пробела, так как внутри функции `@dp.message`)
        indented_code = "\n".join(code_lines)
        return indented_code


component_library = ComponentLibrary()
