import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Clave para que la nube no se ponga mañosa
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

st.set_page_config(page_title="VOXIT CRM")

# URL IDÉNTICA a la que pusiste en Google
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    # Creamos el flujo con tus datos nuevos
    flow = Flow.from_client_config(
        {"web": {
            "client_id": st.secrets["google"]["client_id"], 
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
    
    # Captura el regreso de Google
    if "code" in st.query_params:
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.rerun()
else:
    st.success("✅ ¡CONECTADO, AGUSTÍN!")
    st.balloons()
