import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# ESTA LÍNEA ES MAGIA: Obliga a aceptar la conexión aunque no detecte el HTTPS perfecto
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL exacta: Revisá que en Google Cloud esté IGUAL (con la barra /)
REDIRECT_URI = "https://voxit-crm.streamlit.app"

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
    st.error("Revisá los Secrets en Streamlit Cloud")
    st.stop()

if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    # Usamos un botón normal para que no haya dudas
    st.link_button("🔗 VINCULAR MI GOOGLE DRIVE", auth_url, type="primary")
    
    if "code" in st.query_params:
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.rerun()
else:
    st.success("✅ ¡CONECTADO!")
    st.balloons()
    st.write("Bienvenido al panel, Agustín.")
