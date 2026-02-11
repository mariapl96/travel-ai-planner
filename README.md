# ✈️ Travel AI Planner

Planificador de viajes personalizado con IA que genera itinerarios detallados usando:
- 🤖 **LLM (Llama 3.3 70B)** vía Groq
- 📚 **RAG** (Retrieval Augmented Generation) 
- 🌤️ **APIs externas** (clima en tiempo real)
- ⚡ **Prompt Engineering** avanzado

## 🎯 Características

✅ Generación de itinerarios día por día  
✅ Información actualizada del clima  
✅ Base de conocimiento de 5 destinos europeos  
✅ Personalización por presupuesto, intereses y restricciones  
✅ Recomendaciones gastronómicas específicas  
✅ Presupuestos detallados  

## 🛠️ Stack Tecnológico

- **Frontend:** Streamlit
- **LLM:** Groq API (Llama 3.3 70B)
- **RAG:** LangChain + FAISS + Sentence Transformers
- **APIs:** OpenWeatherMap
- **Lenguaje:** Python 3.11

## 📦 Instalación Local
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/travel-ai-planner.git
cd travel-ai-planner

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API keys
cp .env.example .env
# Editar .env con tus API keys

# Ejecutar aplicación
streamlit run app.py
```

## 🔑 API Keys Necesarias

1. **Groq API:** https://console.groq.com/ (gratis)
2. **OpenWeatherMap:** https://openweathermap.org/api (gratis)

## 🌍 Destinos Disponibles

- 🇫🇷 París
- 🇪🇸 Barcelona
- 🇮🇹 Roma
- 🇪🇸 Madrid
- 🇵🇹 Lisboa

## 📚 Arquitectura RAG
```
Usuario Input → RAG Search (knowledge_base/) → Weather API → LLM → Itinerario
```

## 🎓 Proyecto Académico

Desarrollado para la asignatura de **IA Generativa**  
Master en Inteligencia Artificial  
Enfoque: E1 (Código Avanzado)

## 📄 Licencia

MIT License

## 👤 Autor

María - [Tu GitHub/LinkedIn]