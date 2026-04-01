import streamlit as st
from google_auth_oauthlib.flow import Flow

# Configuración de la página
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# 1. LA URL DEBE SER EXACTAMENTE ESTA (Copiada de tu navegador)
# Si tu app termina en .app, no le agregues nada más.
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

try:
    client_config = {
        "web": {
            "client_id": st.secrets["google"]["client_id"],
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
except:
    st.error("Error en Secrets")
    st.stop()

if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI # <--- ESTA ES LA QUE MANDA
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.link_button("🔗 VINCULAR MI GOOGLE DRIVE", auth_url, type="primary")
    
    # Lógica para capturar el regreso de Google
    if "code" in st.query_params:
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.rerun()
else:
    st.success("¡Conectado!")
    st.write("Panel de Agustín listo.")
