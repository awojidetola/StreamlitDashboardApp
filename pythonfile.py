import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

st.title("CSV Processing and Google Drive Upload Application")

# Google Drive Setup
def authenticate_google_service():
    """Authenticate with Google using credentials from secrets.toml."""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    return build("drive", "v3", credentials=credentials)

drive_service = authenticate_google_service()

# Get folder ID for "Streamlit Folder"
def get_folder_id(service, folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = service.files().list(q=query, spaces="drive").execute()
    folders = response.get("files", [])
    if not folders:
        st.error(f"Folder '{folder_name}' not found in Google Drive.")
        return None
    return folders[0]["id"]

folder_id = get_folder_id(drive_service, "Streamlit Folder")

# File uploader
uploaded_file = st.file_uploader("Select CSV File", type="csv")

# Additional input fields
uploader_name = st.text_input("Enter your name:")
category = st.selectbox("Select the category of the file:", ["Category 1", "Category 2", "Category 3"])
title = st.text_input("Enter the title of the file:")

# Upload button
if st.button("Upload and Save to Google Drive"):
    if uploaded_file and uploader_name and title:
        try:
            # Read the uploaded file
            df = pd.read_csv(uploaded_file)
            
            # Save file temporarily
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Upload to Google Drive
            file_metadata = {
                "name": uploaded_file.name,
                "parents": [folder_id],
            }
            media = MediaFileUpload(temp_file_path, resumable=True)
            uploaded_file_id = drive_service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()["id"]

            # Success message and file details
            st.success("File uploaded successfully to Google Drive!")
            st.write(f"Google Drive File ID: `{uploaded_file_id}`")
            st.write("Preview of the uploaded file:")
            st.dataframe(df.head(5))

            # User inputs
            st.write("Details provided by the uploader:")
            st.write(f"- **Uploader Name:** {uploader_name}")
            st.write(f"- **Category:** {category}")
            st.write(f"- **Title:** {title}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please complete all fields and upload a file before clicking the upload button.")
