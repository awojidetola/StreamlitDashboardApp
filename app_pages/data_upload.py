import streamlit as st
import pandas as pd
from utils.google_services import (
    authenticate_google_service,
    append_to_google_sheet,
    list_subfolders,
    create_subfolder,
    get_subfolder_id,
)
from googleapiclient.http import MediaFileUpload
import datetime

def show_data_upload():
    st.title("Data Upload to Google Drive")

    # Google service authentication
    drive_service = authenticate_google_service(api="drive")
    sheets_service = authenticate_google_service(api="sheets")

    # Folder and sheet configuration
    parent_folder_id = "12EmGxRMyQspzNC5rgtMjozTW0RAWSCfp"  # Replace with your Streamlit folder ID
    sheet_id = "1I9Ezt5JqocHfS9ew2n4PmD3wpbRmhpGwta1jc5PNfJE"  # Replace with your Google Sheet ID
    sheet_name = "DataBank MetaData"

    # Inputs for file upload
    uploaded_file = st.file_uploader("Select CSV File", type="csv")
    uploader_name = st.text_input("Enter your name:")

    # List existing subfolders as categories
    subfolders = list_subfolders(drive_service, parent_folder_id)
    subfolder_names = [folder["name"] for folder in subfolders]
    subfolder_dict = {folder["name"]: folder["id"] for folder in subfolders}

    # Show existing subfolders with an option to create a new category
    category_options = subfolder_names + ["Create New Category"]
    selected_category = st.selectbox("Select the category of the file:", category_options)

    if selected_category == "Create New Category":
        new_category = st.text_input("Enter new category name:")
        category = new_category if new_category else None
    else:
        category = selected_category

    # Title input
    title = st.text_input("Enter the title of the file:")

    # Button to upload file
    if st.button("Upload and Save to Google Drive"):
        if uploaded_file and uploader_name and title and category:
            try:
                # Save the uploaded file temporarily
                uploaded_file.seek(0)  # Reset file pointer to the beginning
                temp_file_path = f"temp_{uploaded_file.name}"

                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.read())  # Write the file content to a temporary file

                # Reset the file pointer again to allow preview
                uploaded_file.seek(0)

                # Preview the first 5 rows of the uploaded file
                try:
                    df = pd.read_csv(uploaded_file)  # Use uploaded_file directly for preview
                    st.write("Preview of uploaded file:")
                    st.dataframe(df.head(5))  # Display the first 5 rows
                except Exception as e:
                    st.warning(f"Could not preview file content. Error: {e}")

                # Check or create a subfolder for the category
                subfolder_id = get_subfolder_id(drive_service, parent_folder_id, category)

                # Upload the file to the subfolder
                file_metadata = {
                    "name": uploaded_file.name,
                    "parents": [subfolder_id],
                }
                media = MediaFileUpload(temp_file_path, mimetype="text/csv", resumable=True)
                uploaded_file_id = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

                # Append metadata to the Google Sheet
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                metadata_row = [timestamp, uploader_name, category, title]
                append_to_google_sheet(
                    sheets_service, spreadsheet_id=sheet_id, sheet_name=sheet_name, row_data=metadata_row
                )

                # Confirm upload
                st.success(f"File uploaded successfully to the '{category}' folder in Google Drive!")

            except Exception as e:
                st.error(f"An error occurred during upload: {e}")
        else:
            st.error("Please complete all fields and upload a file before clicking the upload button.")
