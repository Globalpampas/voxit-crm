import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Configuración de seguridad para la nube
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# --- CONFIGURACIÓN DIRECTA ---
# Usamos tus credenciales aquí para evitar errores de archivos en Render
CLIENT_ID = "549057224304-954k7i0g1afhfe4rbro36ua48hm31kpt.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://voxit-app.onrender.com" # Cambié la URL a la de Render

def crear_flujo():
    return Flow.from_client_config(
        {"web": {
            "client_id": CLIENT_ID, 
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )

# --- LÓGICA DE LA APP ---

if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO CON ÉXITO, AGUSTÍN!")
    st.balloons()
    st.write("### Bienvenido al Panel de VOXIT")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

elif "code" in st.query_params:
    try:
        flow = crear_flujo()
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.query_params.clear()
        st.rerun()
    except Exception:
        st.query_params.clear()
        st.rerun()

else:
    st.title("🚀 VOXIT CRM")
    st.write("Presioná el botón para vincular tu cuenta de Google.")
    
    flow = crear_flujo()
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
