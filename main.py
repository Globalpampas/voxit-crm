import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# La URL que configuramos en Google Cloud
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

# --- LÓGICA DE ACCESO ---
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    # Si volvemos de Google con un código en la URL
    if "code" in st.query_params:
        try:
            flow = crear_flujo()
            flow.fetch_token(code=st.query_params["code"])
            st.session_state.credentials = flow.credentials
            st.query_params.clear() # Limpiamos la URL
            st.rerun()
        except Exception:
            st.error("Error al validar el acceso. Por favor, intentá de nuevo.")
            st.link_button("🔄 REINTENTAR CONEXIÓN", REDIRECT_URI)
            st.stop()
    else:
        # Pantalla inicial: Botón para ir a Google
        flow = crear_flujo()
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")

else:
    # --- PANEL DE CONTROL ---
    st.success("✅ ¡CONECTADO, AGUSTÍN!")
    st.balloons()
    
    st.write("### Bienvenido al CRM")
    if st.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()
