import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_option_menu import option_menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from base_datos import mostrar_base_datos
from generar_qr import generar_qrs

# Cargar configuración desde el archivo .yaml
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Crear el objeto de autenticación
authenticator = stauth.Authenticate(
    config['credentials']['usernames'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Realizar el login
nombre_usuario, autenticado, nombre_rol = authenticator.login("Iniciar sesión", "main")

if not autenticado:
    st.warning("Por favor, inicia sesión para continuar.")
    st.stop()

# Si está autenticado, mostrar el nombre del usuario
st.sidebar.success(f"👋 Bienvenido, {nombre_usuario} ({nombre_rol})")

# Configuración de Google Sheets
info = st.secrets["google_service_account"]
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
cliente = gspread.authorize(credenciales)

# Menú lateral
with st.sidebar:
    menu = option_menu(
        "Menú principal",
        ["Inicio", "Ver Base de Datos", "Generar QR", "Configuración"],
        icons=['house', 'table', 'qr-code', 'gear'],
        menu_icon="cast",
        default_index=0
    )

if menu == "Inicio":
    st.title("🏥 Bienvenido al Sistema de Inventario")
    st.write("Navega usando el menú lateral para ver y gestionar los equipos médicos.")

elif menu == "Ver Base de Datos":
    mostrar_base_datos()

elif menu == "Generar QR":
    generar_qrs()
