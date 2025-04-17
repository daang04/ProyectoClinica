import streamlit as st
import os
import qrcode
from io import BytesIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Usa tus credenciales existentes
info = st.secrets["google_service_account"]
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
cliente = gspread.authorize(credenciales)

# Cliente de Drive
drive_service = build('drive', 'v3', credentials=credenciales)


QR_FOLDER_ID = st.secrets["google_drive"]["qr_folder_id"]


def generar_qrs():
    st.title("📲 Generador de Códigos QR")

    # Obtener archivos existentes en la carpeta QR-equipo
    query = f"'{QR_FOLDER_ID}' in parents and mimeType='image/png'"
    results = drive_service.files().list(q=query, pageSize=1000).execute()
    archivos = results.get('files', [])

    # Obtener el último código generado
    codigos = [f['name'].replace(".png", "") for f in archivos if f['name'].startswith("EQU-")]
    if codigos:
        ultimo = max(codigos)
        siguiente_numero = int(ultimo.split("-")[1]) + 1
    else:
        siguiente_numero = 1

    nuevo_codigo = f"EQU-{siguiente_numero:07d}"
    st.info(f"Se va a generar el siguiente código: **{nuevo_codigo}**")

    if st.button("CREAR"):
        # Crear el QR en memoria
        img = qrcode.make(nuevo_codigo)
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        # Subir a Google Drive
        file_metadata = {
            'name': f"{nuevo_codigo}.png",
            'parents': [QR_FOLDER_ID],
            'mimeType': 'image/png'
        }
        media = MediaIoBaseUpload(buffer, mimetype='image/png')
        archivo = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        st.success(f"✅ QR generado y subido: {nuevo_codigo}")
        st.image(buffer.getvalue(), caption=nuevo_codigo, width=200)
