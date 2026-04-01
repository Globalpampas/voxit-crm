import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# Forzar transporte inseguro para evitar errores de protocolo en el primer login
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL SIN BARRA FINAL (Como pide tu error 400)
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
    st.error("❌ Error: No se encontraron los Secrets. Revisá Settings -> Secrets.")
    st.stop()

if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    flow = Flow.from_client_config(
        client_config,
        scopes=['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/spreadsheets'],
        redirect_uri=REDIRECT_URI
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 VINCULAR MI GOOGLE DRIVE", auth_url, type="primary")
    
    # Captura del código de regreso
    if "code" in st.query_params:
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        st.rerun()
else:
    st.success("✅ ¡CONECTADO CON ÉXITO!")
    st.balloons()
    st.write("Bienvenido Agustín, ya podés usar el sistema.")
