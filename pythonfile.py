import streamlit as st
import pandas as pd

st.title("CSV Processing Application")

# File uploader
uploaded_file = st.file_uploader("Select CSV File", type="csv")

# Additional input fields
uploader_name = st.text_input("Enter your name:")
category = st.selectbox("Select the category of the file:", ["Category 1", "Category 2", "Category 3"])
title = st.text_input("Enter the title of the file:")

# Upload button
if st.button("Upload and Analyse File"):
    if uploaded_file:
        if uploader_name and title:
            try:
                # Read the uploaded CSV into a pandas DataFrame
                df = pd.read_csv(uploaded_file)
                st.success("File uploaded successfully!")

                # Display the first 5 rows of the DataFrame
                st.write("Preview of the first 5 rows:")
                st.dataframe(df.head(5))

                # Print the user inputs
                st.write("Details provided by the uploader:")
                st.write(f"- **Uploader Name:** {uploader_name}")
                st.write(f"- **Category:** {category}")
                st.write(f"- **Title:** {title}")
            except Exception as e:
                st.error(f"An error occurred while reading the file: {e}")
        else:
            st.error("Please provide your name and file title before uploading.")
    else:
        st.error("Please select a file before clicking the upload button.")
