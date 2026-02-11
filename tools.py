"""
Herramientas externas (Tool Use)
APIs para obtener información actualizada
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
            "q": city_name,
            "appid": OPENWEATHER_API_KEY,
            "units": WEATHER_CONFIG["units"],
            "lang": WEATHER_CONFIG["lang"]
        }
        
        # Hacer petición a la API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanzar excepción si hay error
        
        data = response.json()
        
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


def get_weather_forecast(city_name, days=5):
    """
    Obtiene pronóstico del clima para los próximos días
    
    Args:
        city_name (str): Nombre de la ciudad
        days (int): Número de días de pronóstico (máx 5)
        
    Returns:
        str: Pronóstico formateado
    """
    
    try:
        url = WEATHER_CONFIG["forecast_url"]
        params = {
            "q": city_name,
            "appid": OPENWEATHER_API_KEY,
            "units": WEATHER_CONFIG["units"],
            "lang": WEATHER_CONFIG["lang"],
            "cnt": min(days * 8, 40)  # API devuelve datos cada 3h, 8 por día
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Procesar pronóstico (simplificado - tomar 1 dato por día)
        forecast_text = f"\n📅 **Pronóstico para los próximos {days} días:**\n"
        
        # Tomar una lectura por día (mediodía aproximadamente)
        for i in range(0, min(len(data["list"]), days * 8), 8):
            forecast = data["list"][i]
            date = forecast["dt_txt"].split()[0]
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"]
            forecast_text += f"- {date}: {temp}°C, {description}\n"
        
        return forecast_text
        
    except Exception as e:
        return f"⚠️ No se pudo obtener pronóstico: {str(e)}"


# FUNCIÓN OPCIONAL: Búsqueda web (requiere API adicional como SerpAPI o similar)
def web_search(query, num_results=3):
    """
    Búsqueda web para información actualizada
    NOTA: Requiere API de búsqueda (SerpAPI, etc.)
    Esta es una versión placeholder
    
    Args:
        query (str): Consulta de búsqueda
        num_results (int): Número de resultados
        
    Returns:
        str: Resultados formateados
    """
    
    # PLACEHOLDER - Implementar si se añade API de búsqueda
    return """💡 **Sugerencia:** Para información más actualizada sobre precios de vuelos, 
hoteles y eventos, se recomienda consultar:
- Skyscanner / Google Flights (vuelos)
- Booking.com / Airbnb (alojamiento)
- TripAdvisor (reseñas y recomendaciones)
"""


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