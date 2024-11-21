import streamlit as st
from app_pages import dashboards, data_upload, retrieve_data

# Set page configuration
st.set_page_config(page_title="Multi-Page App", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Dashboards", "Data Upload", "Retrieve Data"])  # This defines `page`

# Conditional logic for page selection
if page == "Dashboards":
    dashboards.show_dashboards()
elif page == "Data Upload":
    data_upload.show_data_upload()
elif page == "Retrieve Data":
    retrieve_data.show_retrieve_data()
