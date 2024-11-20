import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import gspread
import pandas as pd
import datetime

# Authenticate Google APIs using Streamlit secrets
def authenticate_google():
    scope = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
    # Use Streamlit secrets for credentials
    credentials_info = st.secrets["google"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    
    # Authenticate Google Drive
    gauth = GoogleAuth()
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)
    
    # Authenticate Google Sheets
    gspread_client = gspread.authorize(credentials)
    return drive, gspread_client

drive, gspread_client = authenticate_google()

# Define the Google Drive folder and Google Sheet
FOLDER_NAME = "Streamlit Folder"
SHEET_NAME = "DataBank Metadata"

# Get the folder ID for the Streamlit Folder
def get_folder_id(drive, folder_name):
    query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    folder_list = drive.ListFile({'q': query}).GetList()
    if folder_list:
        return folder_list[0]['id']
    else:
        st.error(f"Folder '{folder_name}' not found in Google Drive.")
        return None

folder_id = get_folder_id(drive, FOLDER_NAME)

# Create a new metadata row in the Google Sheet
def log_metadata(gspread_client, sheet_name, data_category, data_subcategory, uploaded_by, file_name):
    try:
        sheet = gspread_client.open(sheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        st.error(f"Spreadsheet '{sheet_name}' not found in Google Drive.")
        return False

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata = [file_name, data_category, data_subcategory, uploaded_by, timestamp]
    sheet.append_row(metadata)
    return True

# Upload file to Google Drive
def upload_file_to_drive(file, folder_id):
    uploaded_file = drive.CreateFile({'title': file.name, 'parents': [{'id': folder_id}]})
    uploaded_file.SetContentString(file.read().decode("utf-8"))
    uploaded_file.Upload()
    return uploaded_file['title']

# Streamlit UI
st.title("Data Bank Page")

# Navigation Buttons
upload, download = st.columns(2)

with upload:
    st.subheader("Upload Data")
    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file:
        data_category = st.text_input("Data Category")
        data_subcategory = st.text_input("Data SubCategory")
        uploaded_by = st.text_input("Who uploaded this data?")

        if st.button("Upload File"):
            if data_category and data_subcategory and uploaded_by:
                file_name = upload_file_to_drive(uploaded_file, folder_id)
                if log_metadata(gspread_client, SHEET_NAME, data_category, data_subcategory, uploaded_by, file_name):
                    st.success(f"File '{file_name}' uploaded and metadata logged successfully.")
                else:
                    st.error("Error logging metadata.")
            else:
                st.warning("Please provide all metadata fields before uploading.")

with download:
    st.subheader("Download Data")
    st.markdown(f"[Access the Streamlit Folder in Google Drive](https://drive.google.com/drive/folders/{folder_id})")
