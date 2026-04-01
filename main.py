import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Configuración de la página
st.set_page_config(page_title="VOXIT CRM", page_icon="🚀", layout="centered")

# URL exacta (debe coincidir con Google Cloud)
REDIRECT_URI = "https://voxit-crm.streamlit.app/"

# 1. CARGAR SECRETOS DE STREAMLIT
try:
    client_config = {
        "web": {
            "client_id": st.secrets["google"]["client_id"],
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [REDIRECT_URI]
        }
    }
except Exception as e:
    st.error("❌ Error en los Secrets: Asegurate de haber pegado el client_id y client_secret en Streamlit Cloud.")
    st.stop()

# 2. LÓGICA DE LOGIN / DRIVE
if 'credentials' not in st.session_state:
    st.title("🚀 VOXIT CRM")
    st.subheader("Bienvenido, Agustín")
    st.write("Conectá tu cuenta para empezar a registrar datos.")

    # Configurar el flujo de Google
    flow = Flow.from_client_config(
        client_config,
        scopes=[
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/spreadsheets'
        ],
        redirect_uri=REDIRECT_URI
    )

    # Generar URL de autorización
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    # BOTÓN DE VINCULACIÓN
    st.link_button("🔗 VINCULAR MI GOOGLE DRIVE", auth_url, type="primary")
    
    # Capturar el código que devuelve Google por la URL
    query_params = st.query_params
    if "code" in query_params:
        flow.fetch_token(code=query_params["code"])
        st.session_state.credentials = flow.credentials
        st.success("¡Conexión exitosa!")
        st.rerun()

else:
    # --- LA APP UNA VEZ CONECTADO ---
    st.sidebar.success("Conectado a Google ✅")
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.credentials
        st.rerun()

    st.title("VOXIT CRM 🚀")
    
    tab1, tab2 = st.tabs(["🎙️ Dictar Audio", "📷 Escanear Tarjeta"])

    with tab1:
        st.header("Nuevo Registro por Voz")
        st.info("Pronto: Aquí aparecerá el botón para grabar y procesar con Groq.")
        # Aquí irá la lógica de audio que ya probamos

    with tab2:
        st.header("Escanear con Cámara")
        st.info("Pronto: Aquí podrás sacar fotos a tarjetas y extraer datos con Gemini.")
        # Aquí irá la lógica de cámara que ya probamos
