import streamlit as st
import pandas as pd
from utils.google_services import (
    authenticate_google_service,
    list_subfolders,
    list_files_in_folder,
    download_file,
)
import io

def show_retrieve_data():
    st.title("Retrieve Files by Category")

    # Authenticate Google Drive service
    drive_service = authenticate_google_service(api="drive")
    parent_folder_id = "12EmGxRMyQspzNC5rgtMjozTW0RAWSCfp"  # Replace with your Streamlit Folder ID

    # List subfolders in the parent folder
    subfolders = list_subfolders(drive_service, parent_folder_id)

    if not subfolders:
        st.warning("No categories (subfolders) found in the Streamlit folder.")
    else:
        # Show subfolder names as categories
        categories = {folder["name"]: folder["id"] for folder in subfolders}
        category = st.selectbox("Select the category to retrieve files:", list(categories.keys()))

        if category:
            selected_folder_id = categories[category]
            files = list_files_in_folder(drive_service, selected_folder_id)

            if files:
                # Show file names to select for preview
                file_dict = {file["name"]: file["id"] for file in files}
                selected_file = st.selectbox("Select a file to preview or download:", list(file_dict.keys()))

                if selected_file:
                    file_id = file_dict[selected_file]

                    # Preview Button
                    if st.button("Preview File"):
                        try:
                            # Download and preview file content
                            file_content = download_file(drive_service, file_id)
                            df = pd.read_csv(io.StringIO(file_content.decode("utf-8")))
                            st.dataframe(df.head(5))  # Show first 5 rows
                        except Exception as e:
                            st.error(f"Could not preview the file. Error: {e}")

                    # Download Button
                    st.download_button(
                        label="Download Data",  # Changed label to "Download Data"
                        data=download_file(drive_service, file_id),
                        file_name=selected_file,
                        mime="text/csv"
                    )
            else:
                st.warning(f"No files found in the category: **{category}**")
