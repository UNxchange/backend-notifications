# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import notification
from app.api.graphql.router import graphql_router

#metrics
from app.metrics.prometheus import prometheus_middleware, prometheus_metrics


app = FastAPI(
    title="Notification Service",
    version="1.1.0",
    description="Microservicio de notificaciones con API REST y GraphQL"
)


# Agregar el middleware
app.middleware("http")(prometheus_middleware)

# Incluir routers
app.include_router(notification.router, prefix="/api/v1/notification", tags=["Notification"])
app.include_router(graphql_router, prefix="/api/v1/notification/graphql", tags=["GraphQL"])

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
    return {
        "status": "ok", 
        "service": "unxchange-notification-service",
        "version": "1.1.0",
        "endpoints": {
            "rest_api": "/api/v1/notification/",
            "graphql": "/api/v1/notification/graphql",
            "graphql_playground": "/api/v1/notification/graphql (GET)",
            "docs": "/docs",
            "metrics": "/metrics"
        }
    }

# Endpoint para Prometheus
@app.get("/metrics")
def metrics():
    return prometheus_metrics()