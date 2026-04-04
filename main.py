import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. Ajustes
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# IMPORTANTE: Esta URL debe estar igual en Google Cloud Console
REDIRECT_URI = "https://voxit-app.onrender.com/"

def crear_flujo():
    # Usamos un diccionario para las credenciales para que sea más limpio
    client_config = {
        "web": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    if not client_config["web"]["client_id"]:
        st.error("⚠️ Falta GOOGLE_CLIENT_ID en Environment Variables")
        st.stop()

    return Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )

# --- LÓGICA DE LOGIN ---

# Paso 3: Ya tenemos las credenciales guardadas
if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO!")
    st.balloons()
    st.write(f"### Bienvenido, Agustín")
    if st.sidebar.button("Cerrar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Paso 2: Volvemos de Google con el código en la URL
elif "code" in st.query_params:
    flow = crear_flujo()
    try:
        # Recuperamos el código de la URL
        code = st.query_params["code"]
        flow.fetch_token(code=code)
        st.session_state.credentials = flow.credentials
        st.query_params.clear() # Limpiamos la URL para que no reintente
        st.rerun()
    except Exception as e:
        st.error(f"Error al validar: {e}")
        if st.button("Reintentar"):
            st.query_params.clear()
            st.rerun()

# Paso 1: Pantalla de inicio (Botón de conectar)
else:
    st.title("🚀 VOXIT CRM")
    st.write("Conectá tu cuenta para gestionar Villa Motor Co.")
    
    flow = crear_flujo()
    # Generamos la URL de Google
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 CONECTAR CON GOOGLE", auth_url, type="primary")

st.divider()
st.caption("VOXIT v1.0 - Panel de Control")
