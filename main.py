from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from app.telemetry.router import router as telemetry_router
from app.maintenance.api import router as maintenance_router
from app.procurement.api import router as procurement_router
from app.core.tasks import run_maintenance_scheduler

# Crear la instancia principal de la aplicación FastAPI
app = FastAPI(
    title="Astruxa - Orquestador Industrial 5.0",
    description="Backend para el sistema de monitoreo, control y automatización industrial.",
    version="1.1.0"
)

# Incluir los routers de los diferentes módulos
app.include_router(telemetry_router)
app.include_router(maintenance_router)
app.include_router(procurement_router)

@app.on_event("startup")
@repeat_every(seconds=60 * 60) # Ejecutar cada hora
async def startup_event():
    """
    Al iniciar la aplicación, se activa la tarea recurrente del scheduler.
    """
    await run_maintenance_scheduler()


@app.get("/")
async def root():
    """
    Endpoint raíz para verificar que el servicio está funcionando.
    """
    return {"message": "Astruxa Backend is running!"}


# Si quieres correr esto directamente (aunque usaremos uvicorn desde la terminal)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
