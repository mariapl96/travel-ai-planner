"""
Herramientas externas (Tool Use)
Conecta con las APIs externas para obtener información actualizada
"""

import requests
from config import OPENWEATHER_API_KEY, WEATHER_CONFIG


def get_weather_info(city_name):
    """
    Obtiene información del clima actual de una ciudad
    
    Args:
        city_name (str): Nombre de la ciudad
        
    Returns:
        str: Descripción formateada del clima
    """
    
    try:
        # Construir URL de la API
        url = WEATHER_CONFIG["base_url"]
        params = {
            "q": city_name, # Ciudad seleccionada
            "appid": OPENWEATHER_API_KEY, # Api Key
            "units": WEATHER_CONFIG["units"], # Unidad: Grados Celsius
            "lang": WEATHER_CONFIG["lang"] # Idioma: Español
        }
        
        # Hacer petición a la API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanzar excepción si hay error
        
        data = response.json() # Repuesta en json
        
        # Extraer información relevante
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        
        # Formatear información del clima
        weather_info = f"""🌤️ **Clima actual en {city_name}:**
        - Temperatura: {temp}°C (Sensación térmica: {feels_like}°C)
        - Condiciones: {description.capitalize()}
        - Humedad: {humidity}%
        - Viento: {wind_speed} m/s

        Esta información es actual y debe considerarse al planificar actividades al aire libre.
        """
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        # Si falla la API, devolver mensaje genérico
        return f"""⚠️ No se pudo obtener información del clima actual para {city_name}.
        Se recomienda verificar el clima antes del viaje en sitios como weather.com o accuweather.com.
        """
    except Exception as e:
        return f"⚠️ Error al obtener clima: {str(e)}"


# FUNCIÓN AUXILIAR: Mapeo de ciudades a coordenadas (para mejorar precisión API clima)
CITY_COORDINATES = {
    "París": "Paris,FR",
    "Barcelona": "Barcelona,ES",
    "Roma": "Rome,IT",
    "Madrid": "Madrid,ES",
    "Lisboa": "Lisbon,PT",
}

def get_city_query(city_name):
    """
    Convierte nombre de ciudad a formato óptimo para API
    """
    return CITY_COORDINATES.get(city_name, city_name)