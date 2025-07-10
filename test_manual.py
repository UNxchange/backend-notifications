#!/usr/bin/env python3
"""
Script de prueba para validar el funcionamiento del microservicio de notificaciones
"""

import requests
import json
import sys

# Configuración
BASE_URL = "http://localhost:8002"
NOTIFICATION_ENDPOINT = f"{BASE_URL}/api/v1/notification/usuario-creado/"

def test_notification_endpoint():
    """
    Prueba el endpoint de notificación de usuario creado
    """
    print("🧪 Probando endpoint de notificación de usuario creado...")
    
    # Datos de prueba
    test_user = {
        "name": "Usuario de Prueba",
        "email": "prueba@example.com"
    }
    
    try:
        # Hacer la petición
        response = requests.post(NOTIFICATION_ENDPOINT, json=test_user)
        
        # Verificar respuesta
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Petición exitosa: {result['message']}")
            return True
        else:
            print(f"❌ Error en petición: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se pudo conectar al microservicio")
        print("   Asegúrate de que el servidor esté ejecutándose en http://localhost:8002")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_validation():
    """
    Prueba la validación de datos
    """
    print("\n🧪 Probando validación de datos...")
    
    # Datos inválidos
    invalid_data = {
        "name": "Usuario de Prueba",
        "email": "email-invalido"
    }
    
    try:
        response = requests.post(NOTIFICATION_ENDPOINT, json=invalid_data)
        
        if response.status_code == 422:
            print("✅ Validación funcionando correctamente")
            return True
        else:
            print(f"❌ Validación falló: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en prueba de validación: {e}")
        return False

def check_server_health():
    """
    Verifica que el servidor esté ejecutándose
    """
    print("🩺 Verificando salud del servidor...")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Servidor funcionando correctamente")
            return True
        else:
            print(f"❌ Servidor respondió con: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ No se pudo conectar al servidor: {e}")
        return False

def main():
    """
    Función principal
    """
    print("🚀 Iniciando pruebas del microservicio de notificaciones")
    print("=" * 60)
    
    # Verificar servidor
    if not check_server_health():
        print("\n❌ Las pruebas no pueden continuar sin el servidor funcionando")
        print("   Ejecuta: uvicorn main:app --reload --port 8002")
        sys.exit(1)
    
    # Pruebas
    tests_passed = 0
    total_tests = 2
    
    if test_notification_endpoint():
        tests_passed += 1
    
    if test_validation():
        tests_passed += 1
    
    # Resultados
    print("\n" + "=" * 60)
    print(f"📊 Resultados: {tests_passed}/{total_tests} pruebas pasaron")
    
    if tests_passed == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! El microservicio está funcionando correctamente")
        sys.exit(0)
    else:
        print("❌ Algunas pruebas fallaron. Revisa la configuración y las dependencias")
        sys.exit(1)

if __name__ == "__main__":
    main()
