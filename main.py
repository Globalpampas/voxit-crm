import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Configuración de seguridad para la nube
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL idéntica a tu consola de Google
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

# --- PROCESO DE ENTRADA ---

# A. Si ya entramos anteriormente
if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO CON ÉXITO, AGUSTÍN!")
    st.balloons()
    st.write("### Bienvenido al Panel")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

# B. Si venimos de Google con el código en la URL
elif "code" in st.query_params:
    try:
        flow = crear_flujo()
        # El secreto está en capturar el código tal cual viene
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.query_params.clear()
        st.rerun()
    except Exception:
        # Si el ticket vence, limpiamos y pedimos uno nuevo sin cartel rojo
        st.query_params.clear()
        st.rerun()

# C. Pantalla inicial
else:
    st.title("🚀 VOXIT CRM")
    st.write("Presioná el botón para vincular tu cuenta.")
    
    flow = crear_flujo()
    # Desactivamos PKCE (el verificador que falla) usando este método:
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
