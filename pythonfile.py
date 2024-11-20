import streamlit as st

st.title("CSV Processing Application")
st.file_uploader("Select CSV File", type="csv")
st.button("Upload and Analyse File")