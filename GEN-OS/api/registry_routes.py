@app.get("/api/v1/registry", response_model=RegistryResponse, tags=["Когнитивный Реестр"])
async def get_registry():
    return {"categories": registry.modules}