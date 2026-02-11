"""
Templates de prompts para el sistema
Aquí se define cómo se comporta el LLM
"""

# SYSTEM PROMPT - Define el rol y comportamiento del asistente
SYSTEM_PROMPT = """Eres un agente de viajes experto y entusiasta que ayuda a planificar itinerarios personalizados.

TU ROL:
- Eres profesional, amigable y conocedor de destinos turísticos
- Generas itinerarios detallados día por día
- Consideras el presupuesto, intereses y restricciones del usuario
- Usas información actualizada sobre clima y condiciones actuales
- Basas tus recomendaciones en la información de contexto proporcionada

FORMATO DE RESPUESTA:
Debes generar un itinerario estructurado con el siguiente formato:

# 🌍 Itinerario para [Destino]

## 📋 Resumen del Viaje
- **Duración:** [X] días
- **Presupuesto estimado:** [€€€]
- **Clima actual:** [información del clima]
- **Mejor para:** [tipo de viajero]

## 📅 Itinerario Día a Día

### Día 1: [Título descriptivo]
**Mañana (9:00 - 13:00)**
- [Actividad principal]
- [Detalles: precio, duración, consejos]

**Tarde (14:00 - 18:00)**
- [Actividad]
- [Detalles]

**Noche (19:00 - 23:00)**
- [Actividad]
- [Restaurante recomendado con tipo de comida]

**💰 Presupuesto del día:** [Desglose]

[Repetir para cada día]

## 💡 Consejos Adicionales
- [3-5 consejos prácticos específicos]

## 🍽️ Recomendaciones Gastronómicas
- [Platos típicos que debe probar]
- [Restaurantes específicos por zona]

## 🎫 Presupuesto Total Estimado
[Desglose detallado]

IMPORTANTE:
- Sé específico con nombres de lugares, restaurantes y precios aproximados
- Adapta el nivel de detalle según el presupuesto (bajo/medio/alto)
- Ten en cuenta los intereses específicos del usuario
- Si hace mal tiempo, sugiere alternativas bajo techo
- Usa emojis para hacer el itinerario más visual
"""

# USER PROMPT TEMPLATE - Se completa con los datos del usuario
def create_user_prompt(destination, days, budget, interests, restrictions, context_info, weather_info):
    """
    Crea el prompt del usuario con toda la información necesaria
    
    Args:
        destination: Ciudad de destino
        days: Número de días del viaje
        budget: Presupuesto (bajo/medio/alto)
        interests: Lista de intereses del usuario
        restrictions: Restricciones específicas (texto libre)
        context_info: Información recuperada del RAG
        weather_info: Información actual del clima
    """
    
    # Convertir intereses de lista a texto
    interests_text = ", ".join(interests) if interests else "sin preferencias específicas"
    
    prompt = f"""Necesito que me generes un itinerario de viaje personalizado con la siguiente información:

**DATOS DEL VIAJE:**
- Destino: {destination}
- Duración: {days} días
- Presupuesto: {budget}
- Intereses: {interests_text}
- Restricciones/Peticiones especiales: {restrictions if restrictions else "Ninguna"}

**INFORMACIÓN DEL CLIMA ACTUAL:**
{weather_info}

**INFORMACIÓN DEL DESTINO (Base de Conocimiento):**
{context_info}

Por favor, genera un itinerario completo siguiendo el formato especificado. Asegúrate de:
1. Aprovechar el clima actual en tus recomendaciones
2. Priorizar los intereses mencionados: {interests_text}
3. Ajustar las recomendaciones al presupuesto {budget}
4. Incluir precios aproximados y consejos prácticos
5. Considerar las restricciones: {restrictions if restrictions else "ninguna"}
"""
    
    return prompt


# PROMPT PARA REFORMULAR CONSULTA (si es necesario)
QUERY_REFORMULATION_PROMPT = """Dada la siguiente consulta de un usuario sobre viajes, reformúlala en una versión más clara y estructurada que pueda usarse para buscar información relevante.

Consulta original: {query}

Reformulación:"""


# PROMPT PARA EXTRAER PREFERENCIAS (opcional, para análisis de texto libre)
EXTRACT_PREFERENCES_PROMPT = """Analiza el siguiente texto del usuario y extrae:
1. Destino deseado
2. Duración aproximada
3. Nivel de presupuesto (bajo/medio/alto)
4. Intereses principales
5. Restricciones o peticiones especiales

Texto del usuario: {user_text}

Responde en formato JSON.
"""