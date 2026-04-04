import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. Configuración de seguridad y página
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# 2. URL de redireccionamiento (DEBE coincidir con Google Cloud)
# IMPORTANTE: La barra "/" al final es obligatoria si así está en Google
REDIRECT_URI = "https://voxit-app.onrender.com/"

def crear_flujo():
    # Leemos las variables desde el panel de Render (Environment Variables)
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    # Verificación de seguridad para nosotros
    if not client_id or not client_secret:
        st.error("⚠️ Error: No se encontraron las credenciales en Render.")
        st.info("Revisá que en Render las variables se llamen GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET")
        st.stop()

    return Flow.from_client_config(
        {"web": {
            "client_id": client_id, 
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=[
            'https://www.googleapis.com/auth/drive.file', 
            'https://www.googleapis.com/auth/spreadsheets'
        ],
        redirect_uri=REDIRECT_URI
    )

# --- LÓGICA DE LA APLICACIÓN ---

# CASO A: Ya estamos conectados
if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO CON ÉXITO, AGUSTÍN!")
    st.balloons()
    st.write("### Bienvenido al Panel de Control de VOXIT")
    st.write("Tu sesión con Google Drive y Sheets está activa.")
    
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

# CASO B: Venimos regresando de Google con el código de permiso
elif "code" in st.query_params:
    try:
        flow = crear_flujo()
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials
        # Limpiamos la URL y reiniciamos para entrar al CASO A
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Error al procesar el acceso: {e}")
        if st.button("Reintentar conexión"):
            st.query_params.clear()
            st.rerun()

# CASO C: Pantalla de inicio (Botón de conectar)
else:
    st.title("🚀 VOXIT CRM")
    st.write("Bienvenido, Agustín. Conectá tu cuenta para empezar a gestionar tus prospectos.")
    
    try:
        flow = crear_flujo()
        # Generamos la URL de autorización
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        
        st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")
        
    except Exception as e:
        st.error("Error en la configuración de Google.")
        st.info(f"Detalle técnico: {e}")

# --- PIE DE PÁGINA ---
st.divider()
st.caption("VOXIT CRM - Automatización para Villa Motor Company")
