import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from base_datos import mostrar_base_datos
from generar_qr import generar_qrs
from streamlit_option_menu import option_menu

# Cargar el archivo YAML con la configuración de usuarios y cookies
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Crear el objeto de autenticación
authenticator = stauth.Authenticate(
    config['credentials'],  # Datos de los usuarios
    config['cookie']['name'],  # Nombre de la cookie
    config['cookie']['key'],   # Clave para firmar las cookies
    cookie_expiry_days=config['cookie']['expiry_days'],  # Expiración de cookies
)

# Realizamos el login
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
st.sidebar.success(f"👋 Bienvenido, {name}")

# ---------- AUTENTICACIÓN GOOGLE SHEETS ----------
info = st.secrets["google_service_account"]
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
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

if menu == "Inicio":
    st.title("🏥 Bienvenido al Sistema de Inventario")
    st.write("Navega usando el menú lateral para ver y gestionar los equipos médicos.")

elif menu == "Ver Base de Datos":
    mostrar_base_datos()

elif menu == "Generar QR":
    generar_qrs()
