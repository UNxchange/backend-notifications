# test_notification.py
"""
Test para validar el endpoint de notificación de usuario creado
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importar la aplicación FastAPI

client = TestClient(app)

def test_notify_user_created_success():
    """
    Test para verificar que el endpoint de notificación funciona correctamente
    """
    user_data = {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com"
    }
    
    response = client.post("/api/v1/notification/usuario-creado/", json=user_data)
    
    # Verificar que la respuesta es exitosa
    assert response.status_code == 200
    
    # Verificar la estructura de la respuesta
    json_response = response.json()
    assert "success" in json_response
    assert "message" in json_response
    assert json_response["success"] is True
    assert "juan.perez@example.com" in json_response["message"]

def test_notify_user_created_invalid_email():
    """
    Test para verificar que el endpoint valida correctamente el email
    """
    user_data = {
        "name": "Juan Pérez",
        "email": "email-invalido"
    }
    
    response = client.post("/api/v1/notification/usuario-creado/", json=user_data)
    
    # Verificar que la respuesta es de error de validación
    assert response.status_code == 422

def test_notify_user_created_missing_fields():
    """
    Test para verificar que el endpoint requiere todos los campos
    """
    user_data = {
        "name": "Juan Pérez"
        # email faltante
    }
    
    response = client.post("/api/v1/notification/usuario-creado/", json=user_data)
    
    # Verificar que la respuesta es de error de validación
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__])
