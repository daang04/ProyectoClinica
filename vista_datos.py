import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from base_datos import mostrar_base_datos
from generar_qr import generar_qrs

# Cargar la configuración desde el archivo YAML
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Crear el objeto de autenticación
authenticator = stauth.Authenticate(
    config['credentials'],               # Datos de los usuarios
    config['cookie']['name'],            # Nombre de la cookie
    config['cookie']['key'],             # Clave para firmar las cookies
    config['cookie']['expiry_days']      # Expiración de cookies
)

# Crear el widget de login
name, authentication_status, username = authenticator.login('Login', 'main')

# Si no está autenticado, mostramos un mensaje y detenemos la ejecución
if not authentication_status:
    if authentication_status == False:
        st.error('Username/password is incorrect')  # Si las credenciales no son correctas
    elif authentication_status == None:
        st.warning('Please enter your username and password')  # Si no se ha intentado iniciar sesión
    st.stop()

# Si está autenticado, mostramos el menú lateral y los contenidos
authenticator.logout('Logout', 'main')
st.sidebar.success(f"Bienvenido, {name}")

# ---------- AUTENTICACIÓN GOOGLE SHEETS ----------
# Cargar las credenciales de Google Drive desde secrets
info = st.secrets["google_service_account"]

# Definir el alcance para Google Sheets y Google Drive
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Autorización con las credenciales de Google
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)

# Autenticación con gspread (Google Sheets)
cliente = gspread.authorize(credenciales)

# ---------- MENÚ ----------
with st.sidebar:
    menu = option_menu(
        "Menú principal",
        ["Inicio", "Ver Base de Datos", "Generar QR", "Configuración"],
        icons=['house', 'table', 'qr-code', 'gear'],
        menu_icon="cast",
        default_index=0
    )

# Mostramos el contenido según el menú seleccionado
if menu == "Inicio":
    st.title("🏥 Bienvenido al Sistema de Inventario")
    st.write("Navega usando el menú lateral para ver y gestionar los equipos médicos.")

elif menu == "Ver Base de Datos":
    mostrar_base_datos()

elif menu == "Generar QR":
    generar_qrs()
