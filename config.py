"""
Configuración central del proyecto
Gestiona API keys y parámetros del sistema
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Validar que las API keys existen
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY no encontrada. Asegúrate de tener un archivo .env con tu API key.")

if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY no encontrada. Asegúrate de tener un archivo .env con tu API key.")

# Configuración del modelo LLM
LLM_CONFIG = {
    "model": "llama-3.3-70b-versatile",  # Modelo de Groq
    "temperature": 0.7,  # Creatividad (0 = determinista, 1 = muy creativo)
    "max_tokens": 2048,  # Longitud máxima de respuesta
}

# Configuración del sistema RAG
RAG_CONFIG = {
    "knowledge_base_path": "knowledge_base/",  # Carpeta con archivos de destinos
    "chunk_size": 500,  # Tamaño de fragmentos de texto
    "chunk_overlap": 50,  # Solapamiento entre fragmentos
    "top_k": 3,  # Número de fragmentos relevantes a recuperar
}

# Configuración de embeddings (para RAG)
EMBEDDING_CONFIG = {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",  # Modelo para embeddings
    "device": "cpu",  # Cambiar a "cuda" si tienes GPU
}

# Destinos disponibles en la base de conocimiento
AVAILABLE_DESTINATIONS = [
    "París",
    "Barcelona", 
    "Roma",
    "Madrid",
    "Lisboa"
]

# Configuración de Streamlit
STREAMLIT_CONFIG = {
    "page_title": "✈️ Travel AI Planner",
    "page_icon": "✈️",
    "layout": "wide",
}

# Configuración de la API del clima
WEATHER_CONFIG = {
    "base_url": "http://api.openweathermap.org/data/2.5/weather",
    "forecast_url": "http://api.openweathermap.org/data/2.5/forecast",
    "units": "metric",  # Celsius
    "lang": "es",  # Idioma español
}

print("✅ Configuración cargada correctamente")