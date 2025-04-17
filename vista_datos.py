import streamlit as st
from streamlit_option_menu import option_menu
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from base_datos import mostrar_base_datos
from generar_qr import generar_qrs

# ---------- AUTENTICACIÓN ----------
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