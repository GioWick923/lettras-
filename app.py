import streamlit as st
import google.generativeai as genai
import os

# Configuración de la página
st.set_page_config(page_title="Mi App de IA", layout="centered")

# Título de la app
st.title("🤖 Mi Asistente Inteligente")
st.write("Escribe tu consulta abajo y la IA te responderá.")

# Capturamos la API Key de los secretos de Streamlit (seguridad)
api_key = st.secrets["GOOGLE_API_KEY"]

# Configuramos la IA
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Cuadro de texto para el usuario
user_input = st.text_area("Ingresa tu texto aquí:", height=150)

# Botón para enviar
if st.button("Generar Respuesta"):
    if user_input:
        with st.spinner('La IA está pensando...'):
            try:
                # Aquí puedes agregar instrucciones extra al prompt si quieres
                # Ejemplo: prompt_final = "Responde como un pirata: " + user_input
                response = model.generate_content(user_input)
                st.success("¡Respuesta generada!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor escribe algo antes de enviar.")
