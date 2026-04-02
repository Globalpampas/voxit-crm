import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. PREPARACIÓN: Evitar errores de protocolo en la nube
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# URL EXACTA (Debe coincidir con Google Cloud)
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

# 2. CONFIGURACIÓN DEL FLUJO
def crear_flujo():
    client_config = {
        "web": {
            "client_id": st.secrets["google"]["client_id"], 
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=[
            'https://www.googleapis.com/auth/drive.file', 
            'https://www.googleapis.com/auth/spreadsheets'
        ],
        redirect_uri=REDIRECT_URI
    )

# 3. LÓGICA DE INTERFAZ Y AUTENTICACIÓN
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    
    flow = crear_flujo()
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
    
    # Captura del código de regreso (Con limpieza para evitar el InvalidGrantError)
    if "code" in st.query_params:
        try:
            # Intercambiamos el código por el token real
            flow.fetch_token(code=st.query_params["code"])
            st.session_state.credentials = flow.credentials
            
            # LIMPIEZA: Borramos el código de la URL para que no falle al recargar
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error("El permiso expiró o es inválido. Intentá conectar de nuevo.")
            st.info("Tip: Si el error persiste, probá en una pestaña de Incógnito.")
else:
    # --- PANEL PRINCIPAL (YA CONECTADO) ---
    st.success("✅ ¡CONECTADO, AGUSTÍN!")
    st.balloons()
    
    st.divider()
    st.subheader("Acciones Rápidas")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎙️ Dictar a Google Sheets", use_container_width=True):
            st.info("Módulo de voz listo para configurar.")
    
    with col2:
        if st.button("📷 Escanear Tarjeta", use_container_width=True):
            st.info("Módulo de visión listo para configurar.")

    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()
