import streamlit as st
from chatbot.pipeline.pipeline_controller import PipelineController
import tempfile

@st.cache_resource(show_spinner=False)
def get_pipeline_controller():
    # Create a database session object that points to the URL.
    return PipelineController()

get_pipeline_controller()

st.set_page_config(page_title="Upload Slides")
uploaded_files = st.file_uploader(label="Upload multiple files", type="PDF", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile.write(bytes_data)
        path = tmpfile.name
        pipeline_controller = get_pipeline_controller()
        pipeline_controller.ingest_pdf(path)

    