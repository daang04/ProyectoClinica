import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import *
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

# Crear el widget de login
try:
    name, authentication_status, username = authenticator.login()
except LoginError as e:
    st.error(e)

# Si no está autenticado, mostramos un mensaje y detenemos la ejecución
if not authentication_status:
    st.warning('Por favor, inicia sesión para continuar.')
    st.stop()

# Si está autenticado, mostramos un mensaje de bienvenida
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
