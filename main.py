import streamlit as st
import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Configuración de la página
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# 1. CARGAR SECRETOS DESDE STREAMLIT
try:
    client_config = {
        "web": {
            "client_id": st.secrets["google"]["client_id"],
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["https://voxit-crm.streamlit.app"]
        }
    }
except:
    st.error("❌ Error: No se encontraron los Secrets en Streamlit. Revisá la configuración.")
    st.stop()

# 2. LÓGICA DE AUTENTICACIÓN
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    st.write("Bienvenido, Agustín. Conectá tu Drive para empezar.")
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri='https://voxit-crm.streamlit.app'
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    st.link_button("🔗 VINCULAR MI GOOGLE DRIVE", auth_url)
    
    # Capturar el código de la URL después de volver de Google
    code = st.query_params.get("code")
    if code:
        flow.fetch_token(code=code)
        st.session_state.credentials = flow.credentials
        st.rerun()
else:
    # SI YA ESTÁ CONECTADO, MOSTRAR LA APP
    st.success("✅ Conectado a Google Drive")
    tab1, tab2 = st.tabs(["🎙️ Dictar Audio", "📷 Escanear Tarjeta"])
    
    with tab1:
        st.header("Dictar nuevo registro")
        st.info("Función de audio lista para usar.")
        
    with tab2:
        st.header("Escanear Tarjeta")
        st.info("Función de cámara lista para usar.")
