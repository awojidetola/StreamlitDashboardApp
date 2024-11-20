import streamlit as st
import pandas as pd

st.title("CSV Processing Application")

# File uploader
uploaded_file = st.file_uploader("Select CSV File", type="csv")

# Upload button
if st.button("Upload and Analyse File"):
    if uploaded_file:
        # Read the uploaded CSV into a pandas DataFrame
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            
            # Display the first 5 rows of the DataFrame
            st.write("Preview of the first 5 rows:")
            st.dataframe(df.head(5))
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
    else:
        st.error("Please select a file before clicking the upload button.")
