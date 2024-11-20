import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pandas as pd
import os
import json

# Streamlit Configuration
st.title("File Upload to Google Drive")
st.write("Upload a file and store the details in a Google Sheet.")

# Load Google Cloud credentials from Streamlit secrets
def authenticate_google_service():
    secrets = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(
        secrets,
        scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"],
    )
    return credentials

credentials = authenticate_google_service()

drive_service = build("drive", "v3", credentials=credentials)
sheets_service = build("sheets", "v4", credentials=credentials)

# Google Drive Folder and Sheet Information
drive_folder_name = "Streamlit Folder"
sheet_name = "DataBank MetaData"

# Get folder ID
def get_folder_id(service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, spaces='drive').execute()
    folders = response.get("files", [])
    if not folders:
        st.error(f"Folder '{folder_name}' not found.")
        return None
    return folders[0]["id"]

folder_id = get_folder_id(drive_service, drive_folder_name)

# Upload File Function
def upload_to_drive(file, folder_id, file_name):
    media = MediaFileUpload(file, resumable=True)
    file_metadata = {
        "name": file_name,
        "parents": [folder_id],
    }
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return uploaded_file["id"]

# Append Data to Google Sheets
def append_to_sheet(sheet_service, spreadsheet_name, data):
    sheet_id_query = f"name='{spreadsheet_name}' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false"
    response = drive_service.files().list(q=sheet_id_query, spaces="drive").execute()
    spreadsheet_id = response.get("files", [])[0]["id"]
    
    sheet_data = {"values": [data]}
    sheets_service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1",
        valueInputOption="USER_ENTERED",
        body=sheet_data,
    ).execute()

# Streamlit UI
uploaded_file = st.file_uploader("Choose a file to upload", type=None)
uploader = st.text_input("Enter your name:")
category = st.selectbox("Category of File", ["Category 1", "Category 2", "Category 3"])
title = st.text_input("Enter the file title:")

if st.button("Upload"):
    if uploaded_file and uploader and title:
        try:
            # Save the uploaded file temporarily
            temp_file = f"temp_{uploaded_file.name}"
            with open(temp_file, "wb") as f:
                f.write(uploaded_file.read())

            # Upload file to Google Drive
            file_id = upload_to_drive(temp_file, folder_id, uploaded_file.name)
            st.success(f"File uploaded successfully with ID: {file_id}")

            # Prepare data for the Google Sheet
            upload_date = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = [upload_date, uploader, category, title]
            append_to_sheet(sheets_service, sheet_name, row_data)
            st.success("Data added to Google Sheet successfully!")

            # Cleanup temporary file
            os.remove(temp_file)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please fill all fields and upload a file.")
