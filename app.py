import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Mi App IA", page_icon="✨")

st.title("✨ Mi Aplicación de IA")
st.write("Esta aplicación está conectada a mi cerebro en Google Studio.")

# --- CONEXIÓN CON GOOGLE ---
# Intentamos obtener la clave secreta
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta la API Key. Configúrala en los 'Secrets' de Streamlit.")
    st.stop()

# --- INTERFAZ DE CHAT ---
# Historial de mensajes (para que recuerde la conversación)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE RESPUESTA ---
# Capturar lo que escribe el usuario
if prompt := st.chat_input("Escribe aquí..."):
    # 1. Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Llamar a Google Gemini
    try:
        # Usamos el modelo flash que es rápido
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # AQUÍ PUEDES PEGAR TU PROMPT DE SISTEMA SI QUIERES
        # Ejemplo: instruction = "Eres un experto en cocina. " + prompt
        
        response = model.generate_content(prompt)
        text_response = response.text

        # 3. Mostrar respuesta de la IA
        with st.chat_message("assistant"):
            st.markdown(text_response)
        st.session_state.messages.append({"role": "assistant", "content": text_response})
        
    except Exception as e:
        st.error(f"Error al conectar con Google: {e}")
