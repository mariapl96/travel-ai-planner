"""
Travel AI Planner - Aplicación Principal
Planificador de viajes personalizado con IA, RAG y Tool Use
"""

import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage

# Imports locales
from config import (
    GROQ_API_KEY, 
    LLM_CONFIG, 
    STREAMLIT_CONFIG, 
    AVAILABLE_DESTINATIONS
)
from prompts import SYSTEM_PROMPT, create_user_prompt
from rag_system import RAGSystem
from tools import get_weather_info, get_city_query


# Configuración de la página
st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    page_icon=STREAMLIT_CONFIG["page_icon"],
    layout=STREAMLIT_CONFIG["layout"]
)


# Inicializar sistema RAG (solo una vez)
@st.cache_resource
def initialize_rag():
    """
    Inicializa el sistema RAG (se ejecuta solo una vez)
    """
    return RAGSystem()


# Inicializar LLM (solo una vez)
@st.cache_resource
def initialize_llm():
    """
    Inicializa el modelo de lenguaje Groq
    """
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=LLM_CONFIG["model"],
        temperature=LLM_CONFIG["temperature"],
        max_tokens=LLM_CONFIG["max_tokens"]
    )


def generate_itinerary(destination, days, budget, interests, restrictions, rag_system, llm):
    """
    Genera el itinerario completo usando RAG + LLM + Tool Use
    
    Args:
        destination: Ciudad destino
        days: Número de días
        budget: Nivel de presupuesto
        interests: Lista de intereses
        restrictions: Restricciones del usuario
        rag_system: Sistema RAG inicializado
        llm: Modelo LLM inicializado
        
    Returns:
        str: Itinerario generado
    """
    
    # Paso 1: Obtener información del clima (Tool Use)
    with st.spinner(f"🌤️ Consultando clima actual en {destination}..."):
        city_query = get_city_query(destination)
        weather_info = get_weather_info(city_query)
    
    # Paso 2: Buscar información del destino en RAG
    with st.spinner(f"📚 Buscando información sobre {destination}..."):
        context_info = rag_system.search_by_destination(destination)
    
    # Paso 3: Crear prompt con toda la información
    user_prompt = create_user_prompt(
        destination=destination,
        days=days,
        budget=budget,
        interests=interests,
        restrictions=restrictions,
        context_info=context_info,
        weather_info=weather_info
    )
    
    # Paso 4: Generar itinerario con LLM
    with st.spinner(f"✨ Generando tu itinerario personalizado..."):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        itinerary = response.content
    
    return itinerary


def main():
    """
    Función principal de la aplicación Streamlit
    """
    
    # Header
    st.title("✈️ Travel AI Planner")
    st.markdown("""
    **Planificador de viajes personalizado con IA**  
    Genera itinerarios detallados usando Generación Aumentada por Recuperación (RAG) 
    e información actualizada del clima.
    """)
    
    st.divider()
    
    # Inicializar sistemas
    try:
        rag_system = initialize_rag()
        llm = initialize_llm()
    except Exception as e:
        st.error(f"❌ Error inicializando sistemas: {e}")
        st.stop()
    
    # Sidebar - Formulario de entrada
    with st.sidebar:
        st.header("📝 Planifica tu Viaje")
        
        # Destino
        destination = st.selectbox(
            "🌍 Destino",
            options=AVAILABLE_DESTINATIONS,
            help="Selecciona la ciudad que quieres visitar"
        )
        
        # Duración
        days = st.slider(
            "📅 Duración (días)",
            min_value=1,
            max_value=14,
            value=5,
            help="¿Cuántos días durará tu viaje?"
        )
        
        # Presupuesto
        budget = st.select_slider(
            "💰 Presupuesto",
            options=["Bajo", "Medio", "Alto"],
            value="Medio",
            help="Nivel de presupuesto para el viaje"
        )
        
        # Intereses
        st.markdown("🎯 **Intereses** (selecciona varios)")
        interests = []
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox("🏛️ Cultura", value=True):
                interests.append("Cultura")
            if st.checkbox("🍽️ Gastronomía", value=True):
                interests.append("Gastronomía")
            if st.checkbox("🎨 Arte"):
                interests.append("Arte")
            if st.checkbox("🏖️ Playa"):
                interests.append("Playa")
        
        with col2:
            if st.checkbox("🌳 Naturaleza"):
                interests.append("Naturaleza")
            if st.checkbox("🎉 Vida Nocturna"):
                interests.append("Vida Nocturna")
            if st.checkbox("🛍️ Compras"):
                interests.append("Compras")
            if st.checkbox("⚡ Aventura"):
                interests.append("Aventura")
        
        # Restricciones
        restrictions = st.text_area(
            "📌 Restricciones o peticiones especiales",
            placeholder="Ej: Soy vegetariano, tengo movilidad reducida, viajo con niños...",
            help="Cualquier información adicional que debamos considerar"
        )
        
        st.divider()
        
        # Botón de generar
        generate_button = st.button(
            "🚀 Generar Itinerario",
            type="primary",
            use_container_width=True
        )
    
    # Área principal - Resultados
    if generate_button:
        
        # Validar que hay al menos un interés seleccionado
        if not interests:
            st.warning("⚠️ Por favor, selecciona al menos un interés para personalizar tu itinerario.")
            st.stop()
        
        # Mostrar información del viaje
        st.success(f"✅ Generando itinerario para **{destination}** - {days} días - Presupuesto {budget}")
        
        # Generar itinerario
        try:
            itinerary = generate_itinerary(
                destination=destination,
                days=days,
                budget=budget,
                interests=interests,
                restrictions=restrictions,
                rag_system=rag_system,
                llm=llm
            )
            
            # Mostrar resultado
            st.markdown("---")
            st.markdown(itinerary)
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Itinerario",
                data=itinerary,
                file_name=f"itinerario_{destination.lower()}_{days}dias.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"❌ Error generando itinerario: {e}")
            st.exception(e)
    
    else:
        # Mensaje de bienvenida cuando no hay resultados
        st.info("""
        👈 **Completa el formulario en el panel lateral** para generar tu itinerario personalizado.
        
        **Características:**
        - ✨ Generación con IA (Llama 3.1 70B)
        - 📚 Base de conocimiento actualizada (RAG)
        - 🌤️ Información del clima en tiempo real
        - 💡 Recomendaciones personalizadas
        """)
        
        # Mostrar destinos disponibles
        st.markdown("### 🌍 Destinos Disponibles")
        cols = st.columns(5)
        for i, dest in enumerate(AVAILABLE_DESTINATIONS):
            with cols[i]:
                st.markdown(f"**{dest}**")
        
        # Ejemplo de uso
        with st.expander("📖 Ver ejemplo de uso"):
            st.markdown("""
            **Paso 1:** Selecciona un destino (ej: París)  
            **Paso 2:** Define la duración (ej: 5 días)  
            **Paso 3:** Elige tu presupuesto (Bajo/Medio/Alto)  
            **Paso 4:** Marca tus intereses (Cultura, Gastronomía, etc.)  
            **Paso 5:** Añade restricciones si las hay  
            **Paso 6:** Haz clic en "Generar Itinerario"  
            
            ¡El sistema generará un plan personalizado día a día!
            """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        Desarrollado usando Streamlit, LangChain, Groq y RAG<br>
        Proyecto unidad 1 - IA Generativa
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()