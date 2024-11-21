from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def authenticate_google_service(api="drive"):
    """Authenticate with Google using credentials from secrets.toml."""
    import streamlit as st  # Import here to avoid circular imports
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    return build(api, "v3" if api == "drive" else "v4", credentials=credentials)

def append_to_google_sheet(service, spreadsheet_id, sheet_name, row_data):
    """Append a row of data to a Google Sheet."""
    body = {"values": [row_data]}
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A:D",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()

def list_subfolders(service, parent_id):
    """Retrieve only subfolders within the specified folder."""
    query = f"'{parent_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"
    response = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    return response.get("files", [])

def list_files_in_folder(service, folder_id):
    """List files in a specified folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    response = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    return response.get("files", [])

def create_subfolder(service, parent_id, subfolder_name):
    """Create a subfolder in the specified parent folder."""
    folder_metadata = {
        "name": subfolder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder.get("id")

def get_subfolder_id(service, parent_id, subfolder_name):
    """Retrieve the ID of an existing subfolder or create a new one."""
    subfolders = list_subfolders(service, parent_id)
    subfolder_dict = {folder["name"]: folder["id"] for folder in subfolders}
    if subfolder_name in subfolder_dict:
        return subfolder_dict[subfolder_name]  # Return the ID of the existing subfolder
    else:
        return create_subfolder(service, parent_id, subfolder_name)

def download_file(service, file_id):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    return request.execute()
