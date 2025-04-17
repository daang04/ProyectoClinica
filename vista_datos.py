import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from base_datos import mostrar_base_datos
from generar_qr import generar_qrs
from streamlit_option_menu import option_menu  # Librería para el menú lateral

# Cargar archivo de configuración
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Crear el objeto de autenticación
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Crear el widget de login con todos los parámetros opcionales configurados
try:
    # Crear el widget de login con la ubicación 'main' y otros parámetros
    name, authentication_status, username = authenticator.login(
        location='main',  # Ubicación del formulario (puede ser 'main', 'sidebar', 'unrendered')
        max_concurrent_users=None,  # Sin límite de usuarios concurrentes
        max_login_attempts=None,  # Sin límite de intentos fallidos
        fields={'Username': 'Usuario', 'Password': 'Contraseña', 'Login': 'Iniciar sesión'},  # Personalización de los campos
        captcha=False,  # No usar captcha
        single_session=False,  # Permitimos múltiples sesiones
        clear_on_submit=False,  # No limpiar los campos tras enviar
        key='login_widget'  # Clave única para el widget
    )
except Exception as e:
    st.error(f"Error en el login: {e}")

# Verificar si la autenticación fue exitosa
if authentication_status:
    authenticator.logout('Cerrar sesión', 'sidebar')
    st.sidebar.success(f'👋 Bienvenido, {name}')
    
    # ---------- AUTENTICACIÓN GOOGLE SHEETS ----------
    info = st.secrets["google_service_account"]
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    credenciales = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
    cliente = gspread.authorize(credenciales)

    # ---------- MENÚ LATERAL ----------
    with st.sidebar:
        menu = option_menu(
            "Menú principal",
            ["Inicio", "Ver Base de Datos", "Generar QR", "Configuración"],
            icons=['house', 'table', 'qr-code', 'gear'],
            menu_icon="cast",
            default_index=0
        )

    # Sección de inicio
    if menu == "Inicio":
        st.title("🏥 Bienvenido al Sistema de Inventario")
        st.write("Navega usando el menú lateral para ver y gestionar los equipos médicos.")

    # Sección de base de datos
    elif menu == "Ver Base de Datos":
        mostrar_base_datos()

    # Sección de generar QR
    elif menu == "Generar QR":
        generar_qrs()

else:
    if authentication_status == False:
        st.error('Nombre de usuario/contraseña incorrectos')  # Si las credenciales no son correctas
    elif authentication_status == None:
        st.warning('Por favor, ingresa tu nombre de usuario y contraseña')  # Si no se ha intentado iniciar sesión
