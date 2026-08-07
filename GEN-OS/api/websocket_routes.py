

@app.websocket("/ws/ai-agent")
async def websocket_ai_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Извлекаем tenant_id из параметров запроса (например, ?tenant_id=tenant_0602)
    query_params = websocket.query_params
    tenant_id = query_params.get("tenant_id", "default")

    logger.info(f">>> OMNI_AGENT: Активирован ИИ-канал связи для субъекта [TENANT: {tenant_id}]")

    # Переключаем контекст векторной базы знаний под конкретного клиента
    if tenant_id == "default":
        db_path = str(BASE_DIR / "chroma_db_storage")
        collection_name = "omnifactory_intelligence"
    else:
        db_path = str(BASE_DIR / "tenants_storage" / tenant_id / "chroma_db_storage")
        collection_name = f"omnifactory_intelligence_{tenant_id}"

    try:
        chroma_client = chromadb.PersistentClient(path=db_path)
        collection = chroma_client.get_collection(name=collection_name)
        logger.info(f"✓ [RAG ALIGNED] Подключена изолированная ChromaDB для пространства {tenant_id}")
    except Exception as e:
        logger.warning(f"⚠️ Индекс ChromaDB для {tenant_id} отсутствует или пуст. Инференс в стандартном режиме: {e}")
        collection = None

    try:
        while True:
            raw_data = await websocket.receive_text()

            # Проверяем, не прилетел ли управляющий JSON для инжекции нового промпта
            try:
                parsed_command = json.loads(raw_data)
                if parsed_command.get("action") == "inject_prompt":
                    new_prompt = parsed_command.get("prompt")
                    SYSTEM_PROMPTS_REGISTRY[tenant_id] = new_prompt
                    logger.info(f"🧠 ИИ-ЯДРО: Для {tenant_id} инжектирована новая системная директива.")
                    await websocket.send_text(f"[SYSTEM]: Системная директива ядра OmniAgent успешно обновлена.")
                    continue
            except json.JSONDecodeError:
                user_message = raw_data

            # Извлекаем текущий промпт роли из реестра
            active_instruction = SYSTEM_PROMPTS_REGISTRY.get(tenant_id, SYSTEM_PROMPTS_REGISTRY["default"])
            session_memory = [{"role": "system", "content": active_instruction}]

            # Извлечение контекста из ChromaDB (RAG-контур)
            context_addon = ""
            if collection:
                try:
                    results = collection.query(query_texts=[user_message], n_results=1)
                    if results and results['documents'] and results['documents'][0]:
                        matched_doc = results['documents'][0][0]
                        context_addon = f"\n[ДОКУМЕНТАЛЬНЫЙ КОНТЕКСТ ИЗ БАЗЫ ЗНАНИЙ]: {matched_doc}\n"
                        logger.info("◈ [RAG] Релевантный чанк успешно подмешан в промпт.")
                except Exception as e:
                    logger.error(f"❌ Ошибка выборки ChromaDB: {e}")

            full_prompt = user_message + context_addon
            session_memory.append({"role": "user", "content": full_prompt})

            # Асинхронный вызов локальной модели Ollama
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: ollama.chat(model='codellama', messages=session_memory)
                )

                agent_reply = response['message']['content']
                # Отправляем ответ в реал-тайм стрим логов админки
                await websocket.send_text(agent_reply)

            except Exception as e:
                logger.error(f"Ошибка Ollama Engine: {str(e)}")
                await websocket.send_text(f"[ERROR] Сбой локальной ИИ-ноды: {str(e)}. Проверьте 'ollama run codellama'")

    except WebSocketDisconnect:
        logger.info(f">>> OMNI_AGENT: Сессия связи с {tenant_id} закрыта супервизором.")
