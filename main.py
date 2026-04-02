import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. Configuración de entorno
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL de redirección exacta
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

def crear_flujo():
    return Flow.from_client_config(
        {"web": {
            "client_id": st.secrets["google"]["client_id"], 
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )

# --- PROCESO DE AUTENTICACIÓN ---

# Si ya tenemos las credenciales en la sesión, mostramos el panel
if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO CON ÉXITO!")
    st.balloons()
    st.write("### Bienvenido Agustín")
    st.info("El sistema de Dictado y Escaneo está listo para ser configurado.")
    
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

# Si NO tenemos credenciales, pero Google nos mandó un código en la URL
elif "code" in st.query_params:
    try:
        flow = crear_flujo()
        # Intercambiamos el código por el token real
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        # Limpiamos la URL y forzamos reinicio para que entre al bloque de arriba
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error técnico: {e}")
        st.link_button("🔄 REINTENTAR DESDE CERO", REDIRECT_URI)

# Si NO tenemos nada (Pantalla de inicio)
else:
    st.title("🚀 VOXIT CRM")
    st.write("Estado: Desconectado. Por favor, vinculá tu cuenta.")
    
    flow = crear_flujo()
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
