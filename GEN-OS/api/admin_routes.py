











@app.get("/admin", summary="Рендеринг Контур-Админки Unified Supervisor v8.0")
async def serve_admin(request: Request):
    admin_template = BASE_DIR / "templates" / "admin.html"
    if not admin_template.exists():
        raise HTTPException(status_code=404, detail="Критическая ошибка: файл templates/admin.html не обнаружен.")
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/admin/fragment/dashboard", summary="Получить HTML фрагмент n8n-дашборда")
async def get_dashboard_fragment():
    fragment_path = BASE_DIR / "templates" / "dashboard_fragment.html"
    if not fragment_path.exists():
        return HTMLResponse(content="<div style='color:red;'>Фрагмент dashboard_fragment.html не найден.</div>")
    with open(fragment_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

    @app.get("/api/v1/admin/telemetry")
    async def get_admin_telemetry():
        return {"cpu": round(random.uniform(8.0, 18.0), 1),  "ram": round(random.uniform(2.4, 3.2), 2)}


