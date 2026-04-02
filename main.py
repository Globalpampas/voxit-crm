import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. Configuración de seguridad
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL idéntica a la de tu consola Google
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

# --- LÓGICA DE ENTRADA ---
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    # Si Google nos manda un código, lo procesamos rápido
    if "code" in st.query_params:
        flow = crear_flujo()
        try:
            flow.fetch_token(code=st.query_params["code"])
            st.session_state.credentials = flow.credentials
            st.query_params.clear()
            st.rerun()
        except Exception:
            # Si falla, limpiamos la URL y dejamos que el usuario pruebe de nuevo
            st.query_params.clear()
            st.rerun()

    # Pantalla de inicio limpia
    st.write("Conectá tu cuenta para empezar a trabajar.")
    flow = crear_flujo()
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")

else:
    # --- PANEL AGUSTÍN ---
    st.success("✅ ¡CONECTADO CON ÉXITO!")
    st.balloons()
    st.write("### Bienvenido, Agustín. El sistema está listo.")
    
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()
