import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀", layout="centered")

# IMPORTANTE: Esta URL debe ser IDÉNTICA a la que pusiste en Google Cloud
# Asegurate de que en Google Cloud termine con la barra /
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

# 2. CARGAR CREDENCIALES DESDE LOS SECRETS
try:
    client_config = {
        "web": {
            "client_id": st.secrets["google"]["client_id"],
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
except Exception as e:
    st.error("❌ Error: No se encontraron los 'Secrets' en Streamlit.")
    st.info("Andá a Settings -> Secrets y verificá que estén cargados.")
    st.stop()

# 3. LÓGICA DE AUTENTICACIÓN
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    st.write("Hola Agustín, vinculá tu Drive para empezar a registrar.")

    # Crear el flujo de Google
    flow = Flow.from_client_config(
        client_config,
        scopes=[
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/spreadsheets'
        ],
        redirect_uri=REDIRECT_URI
    )

    # Generar URL de login
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    # Botón de vinculación
    st.link_button("🔗 VINCULAR MI GOOGLE DRIVE", auth_url, type="primary")

    # Capturar el regreso de Google (el código en la URL)
    if "code" in st.query_params:
        try:
            flow.fetch_token(code=st.query_params["code"])
            st.session_state.credentials = flow.credentials
            st.success("¡Conectado con éxito!")
            st.rerun()
        except Exception as e:
            st.error(f"Error al obtener el token: {e}")
else:
    # --- INTERFAZ PRINCIPAL (YA CONECTADO) ---
    st.sidebar.success("Sesión Iniciada ✅")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

    st.title("Panel de Control - VOXIT")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎙️ Iniciar Dictado", use_container_width=True):
            st.info("Función de audio activa (próximamente)")
    with col2:
        if st.button("📷 Escanear Tarjeta", use_container_width=True):
            st.info("Función de cámara activa (próximamente)")

    st.divider()
    st.write("### Últimos Registros")
    st.caption("Aquí se verán los datos sincronizados con tu planilla de Google Sheets.")
