import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Configuración de seguridad
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL de tu app en Render (sacada de tus capturas)
REDIRECT_URI = "https://voxit-app.onrender.com"

def crear_flujo():
    # Usamos los nombres exactos que tenés en tu panel de Render
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        st.error("⚠️ Error: No se encontraron las credenciales en Render. Revisá 'Environment Variables'.")
        st.stop()

    return Flow.from_client_config(
        {"web": {
            "client_id": client_id, 
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )

# --- LÓGICA DE INTERFAZ ---

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
    except Exception as e:
        st.error(f"Error al obtener el token: {e}")
        st.query_params.clear()

else:
    st.title("🚀 VOXIT CRM")
    st.write("Presioná el botón para vincular tu cuenta de Google Drive.")
    
    try:
        flow = crear_flujo()
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
    except Exception as e:
        st.error(f"Error de configuración: {e}")
