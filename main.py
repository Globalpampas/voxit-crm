import streamlit as st
from google_auth_oauthlib.flow import Flow
import os

# 1. Ajustes de seguridad y estética
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀")

# 2. URL de redireccionamiento (Debe ser idéntica a la de Google Cloud)
REDIRECT_URI = "https://voxit-app.onrender.com/"

def crear_flujo():
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        st.error("⚠️ Error: Faltan las credenciales en el panel de Render.")
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

# --- LÓGICA PRINCIPAL ---

# Si ya estamos logueados
if 'credentials' in st.session_state:
    st.success("✅ ¡CONECTADO CON ÉXITO!")
    st.balloons()
    st.write("### Bienvenido al Panel de VOXIT")
    st.info("La conexión con tus planillas de Google está activa.")
    
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        if "flow_steps" in st.session_state:
            del st.session_state.flow_steps
        st.rerun()

# Si volvemos de Google con el código de autorización
elif "code" in st.query_params:
    if "flow_steps" in st.session_state:
        try:
            flow = st.session_state.flow_steps
            flow.fetch_token(code=st.query_params["code"])
            st.session_state.credentials = flow.credentials
            st.query_params.clear()
            st.rerun()
        except Exception as e:
            st.error(f"Error al validar el código: {e}")
            if st.button("Reintentar conexión"):
                st.query_params.clear()
                st.rerun()
    else:
        st.warning("La sesión de seguridad expiró. Intentá de nuevo.")
        if st.button("Volver al Inicio"):
            st.query_params.clear()
            st.rerun()

# Pantalla de inicio
else:
    st.title("🚀 VOXIT CRM")
    st.write("Gestión inteligente para Villa Motor Company.")
    
    flow = crear_flujo()
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    # GUARDAMOS EL FLUJO: Esto evita el error "Missing code verifier"
    st.session_state.flow_steps = flow
    
    st.link_button("🔗 CONECTAR MI GOOGLE DRIVE", auth_url, type="primary")

st.divider()
st.caption("VOXIT v1.0 - Desarrollado para optimización de ventas")
