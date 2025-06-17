# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import notification

app = FastAPI(
    title="Notification Service",
    version="1.0.0"
)

app.include_router(notification.router, prefix="/api/v1/notification", tags=["Notification"])

# Configuración CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint de bienvenida o de health check
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "service": "unxchange-auth-service"}