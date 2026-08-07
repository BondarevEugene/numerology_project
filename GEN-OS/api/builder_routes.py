

@app.post("/api/builder/generate")
async def generate_bot_from_canvas(payload: dict = Body(...)):
    """Прием графической схемы Drawflow и компиляция в реальный aiogram 3.x код"""
    logger.info("◈ [COMPILER] Получен экспорт интерактивного холста.")

    # Генерируем внутреннюю бизнес-логику на основе выстроенных компонентов
    generated_handlers_code = component_library.compile_canvas_flow(payload)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # 1. Сборка файла интеграции Telegram (integrations/telegram.py)
        telegram_runtime_code = (
            "# -*- coding: utf-8 -*-\n"
            "import os\n"
            "import asyncio\n"
            "import logging\n"
            "import ollama\n"
            "from aiogram import Bot, Dispatcher, types\n"
            "from aiogram.utils.keyboard import InlineKeyboardBuilder\n\n"
            "dp = Dispatcher()\n\n"
            "@dp.message()\n"
            "async def handle_canvas_logic(message: types.Message):\n"
            f"{generated_handlers_code}\n\n"
            "async def main():\n"
            "    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_TOKEN'))\n"
            "    await dp.start_polling(bot)\n"
            "if __name__ == '__main__':\n"
            "    asyncio.run(main())\n"
        )
        zip_file.writestr("bot_runtime/integrations/telegram.py", telegram_runtime_code)

        # 2. Манифест и зависимости
        manifest = {"version": "Enterprise 1.2.0",
                    "components_used": list(payload.get("drawflow", {}).get("Home", {}).get("data", {}).keys())}
        zip_file.writestr("bot_runtime/config/manifest.json", json.dumps(manifest, indent=4, ensure_ascii=False))
        zip_file.writestr("bot_runtime/requirements.txt", "aiogram==3.13.1\nollama==0.2.1\n")
        zip_file.writestr("bot_runtime/main.py", "# -*- coding: utf-8 -*-\nfrom integrations import telegram")

    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": "attachment; filename=omnifactory_compiled_bot.zip"}
    )
