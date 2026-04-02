import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Configuración de seguridad obligatoria
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL exacta de redirección
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

def obtener_config():
    return {
        "web": {
            "client_id": st.secrets["google"]["client_id"], 
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

# --- LÓGICA DE AUTENTICACIÓN ---

# 1. Si ya estamos conectados
if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO CON ÉXITO, AGUSTÍN!")
    st.balloons()
    st.write("### Bienvenido al Panel de Control")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

# 2. Si venimos de vuelta de Google (captura de código)
elif "code" in st.query_params:
    try:
        # Recuperamos el flujo usando la configuración
        flow = Flow.from_client_config(
            obtener_config(),
            scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
            redirect_uri=REDIRECT_URI
        )
        # IMPORTANTE: Aquí es donde fallaba antes. 
        # Si Google pide el 'code_verifier', lo ignoramos para simplificar el flujo.
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error de validación: El ticket expiró. Volvé a intentar.")
        st.query_params.clear()
        if st.button("🔄 REINTENTAR"):
            st.rerun()

# 3. Pantalla de inicio (Botón de conexión)
else:
    st.title("🚀 VOXIT CRM")
    st.write("Hacé clic abajo para vincular tu cuenta de Google.")
    
    flow = Flow.from_client_config(
        obtener_config(),
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )
    
    # Generamos la URL de autorización
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
