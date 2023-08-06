import streamlit as st

st.set_page_config(page_title="Upload Slides")
st.file_uploader(label="Upload multiple files",
                 type="PDF", accept_multiple_files=True)
