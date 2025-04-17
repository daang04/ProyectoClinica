import yaml
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from base_datos import mostrar_base_datos
from generar_qr import generar_qrs

# Cargar la configuración desde el archivo YAML
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Crear el objeto de autenticación con los usuarios de la configuración
authenticator = stauth.Authenticate(
    config['credentials']['usernames'],  # Asegúrate de que 'usernames' esté presente
    config['cookie']['name'],            # Nombre de la cookie
    config['cookie']['key'],             # Clave para firmar las cookies
    cookie_expiry_days=config['cookie']['expiry_days'],  # Expiración de cookies
)

# Realizamos el login
nombre_usuario, autenticado, nombre_rol = authenticator.login(form_name="Iniciar sesión", location="main")

# Si no está autenticado, mostramos un mensaje y detenemos la ejecución
if not autenticado:
    st.warning("Por favor, inicia sesión para continuar.")
    st.stop()

# Si está autenticado, obtenemos el nombre del usuario
nombre_usuario = st.session_state["name"]

# ---------- AUTENTICACIÓN GOOGLE SHEETS ----------
info = st.secrets["google_service_account"]
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
cliente = gspread.authorize(credenciales)

# ---------- MENÚ ----------
authenticator.logout("Cerrar sesión", "sidebar")
st.sidebar.success(f"👋 Bienvenido, {nombre_usuario} ({nombre_rol})")

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
