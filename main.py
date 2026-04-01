import streamlit as st
import os.path
import pickle
import json
import pandas as pd
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
from groq import Groq

# --- 1. CONFIGURACIÓN DE APIS ---
GROQ_API_KEY = "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"
client_groq = Groq(api_key=GROQ_API_KEY)

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets', 
          'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid']

def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f: return base64.b64encode(f.read()).decode()
    return ""

logo_base64 = get_base64("logo.jpeg")

# --- 2. CONFIGURACIÓN VISUAL Y CSS ---
st.set_page_config(page_title="VOXIT", page_icon="logo.jpeg", layout="wide")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #101214; }}
    h1, h2, h3, p, span {{ color: #00A89C !important; }}
    [data-testid="stAppViewContainer"] > section:nth-child(2) > div:nth-child(1) {{
        background-image: url("data:image/jpeg;base64,{logo_base64}");
        background-repeat: no-repeat; background-position: center 80px; background-size: 180px; opacity: 0.08; 
    }}
    .titulo-voxit {{ text-align: center; color: #00A89C; font-size: 1.6rem; font-weight: bold; margin-top: -20px; margin-bottom: 25px; }}
    [data-testid="stAudioInput"] {{ width: 90% !important; max-width: 350px !important; margin: 0 auto !important; }}
    [data-testid="stAudioInput"] > div {{ background-color: #1c1f22 !important; border: 2px solid #00A89C !important; border-radius: 30px !important; }}
    .stButton>button {{ background-color: #00A89C !important; color: white !important; font-weight: bold; border-radius: 10px; width: 100%; height: 50px; }}
    .stTextArea textarea {{ background-color: #1c1f22 !important; color: white !important; border: 1px solid #00A89C !important; }}
    [data-testid="stForm"] {{ border: 1px solid #00A89C !important; background-color: #16191c; border-radius: 15px; padding: 15px; }}
    </style>
    <div class="titulo-voxit">🎙️ VOXIT: Entrada Inteligente</div>
    """, unsafe_allow_html=True)

# --- 3. FUNCIONES DE GOOGLE ---
def obtener_servicios():
    if not os.path.exists('token.json'): return None, None, None
    try:
        with open('token.json', 'rb') as token: creds = pickle.load(token)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open('token.json', 'wb') as token: pickle.dump(creds, token)
        return build('drive', 'v3', credentials=creds), build('sheets', 'v4', credentials=creds), build('oauth2', 'v2', credentials=creds)
    except: return None, None, None

def inicializar_estructura(drive, sheets):
    query = "name = 'VOXIT CRM' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    items = drive.files().list(q=query).execute().get('files', [])
    f_id = items[0]['id'] if items else drive.files().create(body={'name': 'VOXIT CRM', 'mimeType': 'application/vnd.google-apps.folder'}, fields='id').execute().get('id')
    q_s = f"name = 'Base de Datos Ventas' and '{f_id}' in parents and trashed = false"
    res = drive.files().list(q=q_s).execute().get('files', [])
    if not res:
        meta = {'name': 'Base de Datos Ventas', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [f_id]}
        ss_id = drive.files().create(body=meta, fields='id').execute().get('id')
        h = [["FECHA", "VENDEDOR", "NOMBRE", "DNI", "MAIL", "TEL", "DIR", "LOC", "ACT", "PROD", "TEXTO"]]
        sheets.spreadsheets().values().update(spreadsheetId=ss_id, range="A1", valueInputOption="RAW", body={'values': h}).execute()
        return ss_id
    return res[0]['id']

# --- 4. MOTOR DE IA ---
def transcribir_audio(archivo):
    return client_groq.audio.transcriptions.create(file=("dictado.wav", archivo.read()), model="whisper-large-v3-turbo", response_format="text")

def procesar_con_ia(texto):
    p = f"Extrae datos de venta en JSON: {{\"nombre\": \"-\", \"dni\": \"-\", \"mail\": \"-\", \"tel\": \"-\", \"dir\": \"-\", \"loc\": \"-\", \"act\": \"-\", \"prod\": \"-\"}}. Texto: \"{texto}\". SOLO el JSON."
    res = client_groq.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": p}], response_format={"type": "json_object"})
    return json.loads(res.choices[0].message.content)

# --- 5. LÓGICA DE INTERFAZ ---
# Usamos un contador para forzar el reseteo de componentes
if 'count' not in st.session_state: st.session_state.count = 0
if 'texto' not in st.session_state: st.session_state.texto = ""

servicios = obtener_servicios()
drive, sheets, auth = servicios if servicios else (None, None, None)

if drive is None:
    st.title("🚀 VOXIT CRM")
    if st.button("🔗 CONECTAR GOOGLE"):
        if os.path.exists('client_secret.json'):
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'wb') as token: pickle.dump(creds, token)
            st.rerun()
else:
    try:
        user = auth.userinfo().get().execute()
        ss_id = inicializar_estructura(drive, sheets)
        
        st.sidebar.info(f"Usuario: {user.get('email')}")
        sheet_link = f"https://docs.google.com/spreadsheets/d/{ss_id}"
        st.sidebar.markdown(f'<a href="{sheet_link}" target="_blank"><button style="width:100%; background-color:#00A89C; color:white; border:none; padding:10px; border-radius:5px; font-weight:bold;">📂 VER EXCEL</button></a>', unsafe_allow_html=True)

        # 1. AUDIO (Con key dinámica para limpiar)
        st.write("### 1. Grabar Reporte")
        audio = st.audio_input("Toca para dictar...", key=f"audio_{st.session_state.count}")
        if audio:
            with st.spinner("Transcribiendo..."):
                st.session_state.texto = transcribir_audio(audio)

        # 2. FORMULARIO
        st.write("### 2. Validar Datos")
        with st.form(key=f"form_{st.session_state.count}", clear_on_submit=True):
            t_ed = st.text_area("Texto detectado:", value=st.session_state.texto, height=120)
            if st.form_submit_button("🚀 REGISTRAR AHORA"):
                if t_ed:
                    with st.spinner("Guardando..."):
                        d = procesar_con_ia(t_ed)
                        fila = [datetime.now().strftime("%d/%m/%Y %H:%M"), user.get('name', 'Vendedor'), 
                                d.get('nombre'), d.get('dni'), d.get('mail'), d.get('tel'),
                                d.get('dir'), d.get('loc'), d.get('act'), d.get('prod'), t_ed]
                        sheets.spreadsheets().values().append(spreadsheetId=ss_id, range="A1", valueInputOption="RAW", body={'values': [fila]}).execute()
                        
                        # Limpieza absoluta: cambiamos el ID de los componentes
                        st.session_state.texto = ""
                        st.session_state.count += 1 
                        st.success("¡Venta Guardada!")
                        st.rerun()

        if st.button("🗑️ LIMPIAR TODO"):
            st.session_state.texto = ""
            st.session_state.count += 1
            st.rerun()

        # 3. TABLA DE REGISTROS (Recuperada)
        st.markdown("---")
        st.write("### 📊 Últimos Registros")
        res = sheets.spreadsheets().values().get(spreadsheetId=ss_id, range="A1:K20").execute()
        if res.get('values'):
            df = pd.DataFrame(res.get('values')[1:], columns=res.get('values')[0])
            st.dataframe(df.tail(5), use_container_width=True)

    except Exception as e: st.error(f"Error: {e}")