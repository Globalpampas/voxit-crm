import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Forzar transporte seguro
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL que debe coincidir con tu consola de Google
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

# --- INICIO DE LA APP ---
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    # Si hay un código en la URL, intentamos validarlo
    if "code" in st.query_params:
        try:
            flow = crear_flujo()
            flow.fetch_token(code=st.query_params["code"])
            st.session_state.credentials = flow.credentials
            # Limpiamos la URL y reiniciamos para entrar al panel
            st.query_params.clear()
            st.rerun()
        except Exception:
            # Si el código falló, limpiamos la URL y mostramos el botón de nuevo
            st.query_params.clear()
            st.error("El ticket de acceso expiró. Vamos de nuevo:")
            st.rerun()
    
    # Pantalla de conexión limpia
    st.write("Conectá tu cuenta para empezar a trabajar.")
    flow = crear_flujo()
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")

else:
    # --- PANEL AGUSTÍN ---
    st.success("✅ ¡CONECTADO CON ÉXITO!")
    st.balloons()
    
    st.write(f"### Panel de Control - Agustín")
    st.info("Ya podés usar las funciones de Dictado y Escaneo.")
    
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()
