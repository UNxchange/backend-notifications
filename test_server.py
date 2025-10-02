# test_server.py - Versión simplificada para probar
from fastapi import FastAPI

app = FastAPI(
    title="Notification Service Test",
    version="1.0.0",
    description="Servidor de prueba para notificaciones"
)

@app.get("/")
def read_root():
    return {
        "status": "ok", 
        "service": "unxchange-notification-service-test",
        "message": "🚀 Servidor funcionando correctamente!"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "notifications"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)