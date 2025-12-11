
import streamlit as st
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="LyricalFlow Web",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS VISUALES (CSS) ---
# Aquí configuramos el fondo negro y los colores de letra
st.markdown("""
    <style>
    /* Fondo oscuro casi negro (20, 20, 20) */
    .stApp {
        background-color: #141414;
    }
    
    /* Estilo base del texto (no activo) */
    .lyrics-line {
        font-family: Arial, sans-serif;
        font-size: 24px;
        color: rgba(255, 255, 255, 0.3); /* Blanco transparente */
        text-align: center;
        padding: 10px;
        transition: all 0.5s ease;
    }

    /* Estilo de la línea ACTIVA (Color Crema y Grande) */
    .active-line {
        font-size: 40px;
        font-weight: bold;
        color: #eeefbe; /* Tu color crema */
        text-shadow: 0px 0px 10px rgba(238, 239, 190, 0.5);
        padding: 20px;
    }
    
    /* Ocultar elementos de Streamlit que no sirven aquí */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- DATOS (TU LETRA) ---
LETRA_CANCION = """This is the rhythm of the night
The night, oh, yeah
The rhythm of the night
This is the rhythm of my life
My life, oh, yeah
The rhythm of my life
Oh, yeah
I know you wanna say it
But you can't find the words
To tell me how you feel
"""

lines = [line for line in LETRA_CANCION.split('\n') if line.strip()]

# --- LÓGICA DE CONTROL ---
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'playing' not in st.session_state:
    st.session_state.playing = False

# Contenedor principal centrado
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True) # Espacio arriba
    
    # Botón de control (Play/Pause)
    if st.button("⏯️ PLAY / PAUSA", use_container_width=True):
        st.session_state.playing = not st.session_state.playing

    st.markdown("---")

    # Bucle para dibujar las líneas
    # Mostramos 2 líneas antes y 2 después para dar contexto
    current = st.session_state.index
    
    for i in range(max(0, current - 2), min(len(lines), current + 3)):
        line_text = lines[i]
        
        if i == current:
            # Línea actual (Resaltada)
            st.markdown(f'<div class="lyrics-line active-line">{line_text}</div>', unsafe_allow_html=True)
        else:
            # Líneas secundarias
            st.markdown(f'<div class="lyrics-line">{line_text}</div>', unsafe_allow_html=True)

# --- AUTOMATIZACIÓN (El "Game Loop") ---
if st.session_state.playing:
    time.sleep(3) # Espera 3 segundos (Velocidad del auto)
    
    if st.session_state.index < len(lines) - 1:
        st.session_state.index += 1
        st.rerun() # Recarga la página para mostrar la siguiente línea
    else:
        st.session_state.playing = False
        st.session_state.index = 0 # Reiniciar al final
        st.rerun()
